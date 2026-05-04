import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile

st.set_page_config(page_title="JAHS Emoji Factory", page_icon="🦁", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #0f172a; color: #f8fafc;}
    h1, h2, h3 {color: #deff9a;}
    .stButton>button {background-color: #deff9a; color: #0f172a; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.title("🦁 JAHS 全自动切割与适配工厂 (零成本版)")
st.markdown("将包含多个 JAHS 表情的网格图上传，系统将自动裁切、居中、透明填充，并输出符合平台规范的 ZIP 包。")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 第一步：上传网格原图")
    uploaded_file = st.file_uploader("支持 JPG, PNG 格式", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGBA")
        st.image(image, caption="原始网格图预览", use_container_width=True)

with col2:
    st.subheader("⚙️ 第二步：切割与平台规则设定")
    rows = st.number_input("原图包含几行？", min_value=1, value=2)
    cols = st.number_input("原图包含几列？", min_value=1, value=3)
    
    platform = st.selectbox("目标发布平台", ["微信表情包 (240x240)", "LINE (370x320)"])
    if "微信" in platform:
        target_w, target_h = 240, 240
    else:
        target_w, target_h = 370, 320

st.divider()

if uploaded_file is not None:
    if st.button("✂️ 开始智能裁切与规格适配"):
        with st.spinner('🦞 Openclew 切割机运行中...'):
            img_width, img_height = image.size
            cell_width = img_width // cols
            cell_height = img_height // rows
            
            # 创建在内存中的 ZIP 文件
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                
                count = 1
                for r in range(rows):
                    for c in range(cols):
                        # 1. 精确裁切出每一个表情
                        left = c * cell_width
                        top = r * cell_height
                        right = (c + 1) * cell_width
                        bottom = (r + 1) * cell_height
                        cropped_img = image.crop((left, top, right, bottom))
                        
                        # 2. 等比例缩放并自动填充透明背景 (Padding)
                        cropped_img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
                        final_img = Image.new("RGBA", (target_w, target_h), (255, 255, 255, 0)) # 透明背景
                        
                        # 计算居中位置
                        paste_x = (target_w - cropped_img.width) // 2
                        paste_y = (target_h - cropped_img.height) // 2
                        final_img.paste(cropped_img, (paste_x, paste_y))
                        
                        # 3. 存入内存 ZIP
                        img_byte_arr = io.BytesIO()
                        final_img.save(img_byte_arr, format='PNG')
                        zip_file.writestr(f"JAHS_Emoji_{count}.png", img_byte_arr.getvalue())
                        count += 1

            st.success(f"✅ 成功提取并处理了 {rows * cols} 个独立表情！")
            
            # 提供下载按钮
            st.download_button(
                label="📦 一键下载符合规格的表情包压缩文件 (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="JAHS_Ready_Emojis.zip",
                mime="application/zip"
            )
