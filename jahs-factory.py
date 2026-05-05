import streamlit as st
from PIL import Image, ImageFilter
from rembg import remove
import io
import zipfile

st.set_page_config(page_title="JAHS Emoji Factory PRO", page_icon="🦁", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #0f172a; color: #f8fafc;}
    h1, h2, h3 {color: #deff9a;}
    .stButton>button {background-color: #deff9a; color: #0f172a; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.title("🦁 JAHS 全自动抠图与描边工厂 (PRO版)")
st.markdown("不仅切割！系统将利用 AI **全自动去除白底**，并添加符合 LINE/微信 规范的 **2px 白色描边**。")
st.divider()

# 自定义函数：沿着透明通道添加 2px 白色描边
def add_white_stroke(img, stroke_size=2):
    img = img.convert("RGBA")
    # 提取透明通道 (Alpha)
    alpha = img.split()[3]
    # 扩张透明通道轮廓
    dilated_alpha = alpha.filter(ImageFilter.MaxFilter(stroke_size * 2 + 1))
    # 创建一个纯白图层
    stroke_img = Image.new("RGBA", img.size, (255, 255, 255, 255))
    # 将扩张后的轮廓赋予纯白图层
    stroke_img.putalpha(dilated_alpha)
    # 把抠好的狮子原图叠加上去
    stroke_img.alpha_composite(img)
    return stroke_img

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 第一步：上传网格原图")
    uploaded_file = st.file_uploader("请上传带有白底的 AI 网格图", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGBA")
        st.image(image, caption="原始排版图", use_container_width=True)

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
    if st.button("✂️ 启动 AI 抠图、描边与适配"):
        with st.spinner('🦞 Openclew AI 视觉引擎正在剥离背景并生成描边，请稍候...'):
            img_width, img_height = image.size
            cell_width = img_width // cols
            cell_height = img_height // rows
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                
                count = 1
                for r in range(rows):
                    for c in range(cols):
                        # 1. 物理切割
                        left = c * cell_width
                        top = r * cell_height
                        right = (c + 1) * cell_width
                        bottom = (r + 1) * cell_height
                        cropped_img = image.crop((left, top, right, bottom))
                        
                        # 2. AI 智能抠图 (去除背景变透明)
                        no_bg_img = remove(cropped_img)
                        
                        # 3. 添加 2px 白色描边
                        stroked_img = add_white_stroke(no_bg_img, stroke_size=2)
                        
                        # 4. 缩放并居中到透明画布上
                        stroked_img.thumbnail((target_w - 10, target_h - 10), Image.Resampling.LANCZOS)
                        final_img = Image.new("RGBA", (target_w, target_h), (255, 255, 255, 0)) # 绝对透明底
                        
                        paste_x = (target_w - stroked_img.width) // 2
                        paste_y = (target_h - stroked_img.height) // 2
                        final_img.paste(stroked_img, (paste_x, paste_y))
                        
                        # 5. 打包入 ZIP
                        img_byte_arr = io.BytesIO()
                        final_img.save(img_byte_arr, format='PNG')
                        zip_file.writestr(f"JAHS_Emoji_{count}.png", img_byte_arr.getvalue())
                        count += 1

            st.success(f"✅ 成功提取了 {rows * cols} 个表情，已完美透明化并添加 2px 描边！")
            
            st.download_button(
                label="📦 一键下载完美版表情包压缩文件 (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="JAHS_Ready_Emojis_PRO.zip",
                mime="application/zip"
            )
