import streamlit as st
import time

# ==========================================
# 1. 网页全局设置
# ==========================================
st.set_page_config(
    page_title="JAHS Emoji Factory",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 让界面更贴合 JAHS 的现代感
st.markdown("""
    <style>
    .main {background-color: #0f172a; color: #f8fafc;}
    h1, h2, h3 {color: #deff9a;}
    .stButton>button {background-color: #deff9a; color: #0f172a; font-weight: bold; border-radius: 8px;}
    .stButton>button:hover {background-color: #bef264;}
    .stTextInput>div>div>input {border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

st.title("🦁 JAHS 基哈狮自动化表情包工厂")
st.markdown("基于 **Openclew** 逻辑的 IP 生产控制台 | *The Homecoming Adventure*")
st.divider()

# ==========================================
# 2. 侧边栏：核心基因锁 (The Gene Lock)
# ==========================================
with st.sidebar:
    st.header("🧬 V.I. 基因锁设定")
    st.markdown("这些底层参数将被强制写入每一次生产，确保形象 **100% 一致**。")
    
    lora_weight = st.slider("JAHS LoRA 模型权重", 0.0, 1.0, 0.85, 0.05)
    
    st.subheader("底层视觉特征 (不可变)")
    base_prompt = st.text_area(
        "Visual Identity", 
        "chibi lion, fluffy deep orange mane, light beige face, thick black eyebrows, wearing a black hexagram star necklace, vector illustration style, thick clean outlines, flat colors, cute and healing vibe, transparent background", 
        height=180
    )
    
    st.info("💡 **系统提示**：此处的设定旨在挂载您未来的 JAHS 专属模型。")

# ==========================================
# 3. 主操作区：本周生产线 (The Production Line)
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎬 步骤 1: 设定动作与情绪")
    category = st.selectbox(
        "选择本周生产线系列", 
        ["🙏 信仰与敬拜 (Worship/Faith)", "🎸 音乐与艺术 (Music/Live)", "💼 日常与职场 (Daily Social)", "🌍 全球旅拍 (Global Pilgrimage)"]
    )
    action_input = st.text_input("输入具体的动作描述", placeholder="例如：双手合十，闭目祈祷，头顶有柔和光环")
    
with col2:
    st.subheader("📝 步骤 2: 文字与格式适配")
    text_input = st.text_input("表情包配文 (自动排版)", placeholder="例如：阿门！ / Amen")
    platform = st.selectbox(
        "目标分发平台规格", 
        ["微信表情包 (240x240, 动图 GIF)", "LINE Creators (最大 370x320, APNG)", "高清社交海报 (1024x1024, PNG)"]
    )

# ==========================================
# 4. 执行与输出区 (Openclew Core)
# ==========================================
st.divider()

if st.button("🚀 启动龙虾系统生成 (Generate)"):
    if not action_input:
        st.warning("⚠️ 报告情报官：请输入具体的动作描述才能启动生产！")
    else:
        with st.spinner('🦞 Openclew 逻辑脱壳与重组中...'):
            time.sleep(1.5) # 模拟处理时间
            
            st.success("✅ 生产指令已就绪！")
            
            # 整合最终的结构化 Prompt
            final_prompt = f"(masterpiece, best quality), 1boy, {base_prompt}, {action_input}, text '{text_input}', <lora:JAHS_Official_v1:{lora_weight}>"
            
            st.subheader("⚙️ 标准化生图参数 (供专属绘图节点使用)")
            st.code(final_prompt, language="text")
            
            st.markdown("### 🖼️ 预览区 (API 占位符)")
            st.info(f"**技术架构说明**：当您在后台配置好 Stable Diffusion API 或接通 ComfyUI 工作流后，系统将直接根据上述参数，在此处渲染出符合 {platform} 规格的 JAHS 图片。")
            
            # 模拟数据输出展示
            st.json({
                "Character": "JAHS (Kihah)",
                "Series": category,
                "Action": action_input,
                "Text_Overlay": text_input,
                "Target_Platform": platform,
                "Status": "Ready for API Rendering"
            })
