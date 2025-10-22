import streamlit as st
from PIL import Image
from config import configure_gemini, get_gemini_model
from templates import get_header_html, get_footer_html, get_success_html, get_error_html
from prompts import CHEMISTRY_PROMPT



# Clean, reliable solution card
def display_solution(response_text, subject="Physics"):
    icon = "⚛️" if subject == "Physics" else "🧪"
    
    with st.container():
        st.markdown(f"""
        <div style="
            background: #f8fafc;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        ">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                <span style="font-size: 1.2rem;">{icon}</span>
                <h3 style="margin: 0; color: #2d3748;">{subject} Solution</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Content in a clean container
        st.markdown(response_text)
        
        st.markdown("""
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; color: #718096; font-size: 0.9rem;">
                Educational Solution • Powered by Gemini AI
            </div>
        </div>
        """, unsafe_allow_html=True)


# First load the font
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Simple CSS for basic styling
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 16px;
        height: 60px;
        font-family: "Cairo", sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        border: none;
        background: linear-gradient(135deg, #34a853, #0f9d58);
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(52, 168, 83, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Set page config for mobile
st.set_page_config(
    page_title="اشرحلي",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Header
st.markdown(get_header_html(), unsafe_allow_html=True)

# Initialize session state
if 'api_configured' not in st.session_state:
    st.session_state.api_configured = False

# Configure Gemini
st.session_state.api_configured = configure_gemini()

# SIMPLE WORKING FILE UPLOADER
st.markdown("""
<div style='
    background: white;
    border-radius: 20px;
    padding: 2.5rem 1.5rem;
    margin: 1.5rem 0;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    border: 2px dashed #1a73e8;
'>
    <div style='
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-size: 2.5rem;
        color: white;
        box-shadow: 0 8px 20px rgba(26, 115, 232, 0.3);
    '>
        📁
    </div>
    <div style='
        font-family: "Cairo", sans-serif;
        color: #1a73e8;
        margin: 0 0 0.5rem;
        font-size: 1.4rem;
        font-weight: 700;
    '>رفع التمرين</div>
    <div style='
        font-family: "Cairo", sans-serif;
        color: #5f6368;
        margin: 0;
        font-size: 1rem;
        line-height: 1.5;
    '>استخدم الزر أدناه لرفع صورة من هاتفك</div>
</div>
""", unsafe_allow_html=True)

# NATIVE STREAMLIT FILE UPLOADER - GUARANTEED TO WORK
uploaded_file = st.file_uploader(
    "اختر صورة التمرين",
    type=['png', 'jpg', 'jpeg'],
    help="PNG, JPG, JPEG - حتى 200MB"
)

# Show selected file info
if uploaded_file is not None:
    st.markdown(f"""
    <div style='
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #34a853;
        font-family: "Cairo", sans-serif;
        text-align: center;
    '>
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">✅</div>
        <div style="color: #1a73e8; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">تم رفع الملف بنجاح!</div>
        <div style="color: #5f6368; font-size: 0.95rem;">{uploaded_file.name}</div>
        <div style="color: #9aa0a6; font-size: 0.8rem; margin-top: 0.5rem;">حجم الملف: {uploaded_file.size / 1024 / 1024:.1f} MB</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    # Solve button
    if st.button("🚀 حل التمرين الآن", type="primary", use_container_width=True):
        if not st.session_state.api_configured:
            st.markdown(get_error_html("حدث خطأ في الإعدادات"), unsafe_allow_html=True)
        else:
            with st.spinner("🔬 جاري تحليل التمرين..."):
                try:
                    model = get_gemini_model()
                    response = model.generate_content([CHEMISTRY_PROMPT, image])
                    
                    st.markdown(get_success_html(), unsafe_allow_html=True)
                    st.markdown("---")
                    
               # Minimal and clean version

                    
                    # Usage
                    display_solution(response.text, "Physics")
                except Exception as e:
                    st.markdown(get_error_html(f"خطأ في التحليل: {str(e)}"), unsafe_allow_html=True)
                    st.info("📱 تأكد من جودة الصورة ووضوح النص")

# Footer
st.markdown(get_footer_html(), unsafe_allow_html=True)

# Clean, reliable solution card
def display_solution(response_text, subject="Physics"):
    icon = "⚛️" if subject == "Physics" else "🧪"
    
    with st.container():
        st.markdown(f"""
        <div style="
            background: #f8fafc;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        ">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
                <span style="font-size: 1.2rem;">{icon}</span>
                <h3 style="margin: 0; color: #2d3748;">{subject} Solution</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Content in a clean container
        st.markdown(response_text)
        
        st.markdown("""
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; color: #718096; font-size: 0.9rem;">
                Educational Solution • Powered by Gemini AI
            </div>
        </div>
        """, unsafe_allow_html=True)

