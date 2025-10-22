import streamlit as st
from PIL import Image
from config import configure_gemini, get_gemini_model
from templates import get_header_html, get_footer_html, get_success_html, get_error_html
from prompts import CHEMISTRY_PROMPT

# Load the font
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Custom CSS for modern mobile design
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Completely hide the file uploader */
    .stFileUploader {
        display: none !important;
    }
    
    /* Hide file uploader label */
    .stFileUploader > label {
        display: none !important;
    }
    
    /* Custom upload button */
    .custom-upload-button > button {
        width: 100%;
        border-radius: 20px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 2px dashed #1a73e8;
        background: white;
        transition: all 0.3s ease;
        cursor: pointer;
        font-family: "Cairo", sans-serif;
        color: #1a73e8;
        font-size: 1.4rem;
        font-weight: 700;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .custom-upload-button > button:hover {
        border-color: #0d47a1;
        background: #f8fbff;
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(26, 115, 232, 0.15);
    }
    
    .upload-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        color: white;
        box-shadow: 0 8px 20px rgba(26, 115, 232, 0.3);
        transition: all 0.3s ease;
    }
    
    .custom-upload-button > button:hover .upload-icon {
        transform: scale(1.05);
        box-shadow: 0 12px 25px rgba(26, 115, 232, 0.4);
    }
    
    .upload-title {
        color: #1a73e8;
        margin: 0;
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    .upload-subtitle {
        color: #5f6368;
        margin: 0;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    .upload-hint {
        color: #9aa0a6;
        margin: 0.5rem 0 0;
        font-size: 0.85rem;
    }
    
    /* Solve button styling */
    .stButton > button:not(.custom-upload-button > button) {
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
        transition: all 0.3s ease;
    }
    
    .stButton > button:not(.custom-upload-button > button):hover {
        background: linear-gradient(135deg, #2e8b47, #0d8040);
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(52, 168, 83, 0.4);
    }
    
    /* File info card */
    .file-info-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #34a853;
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

# Create the file uploader first (it will be hidden by CSS)
uploaded_file = st.file_uploader(
    "رفع صورة التمرين",
    type=['png', 'jpg', 'jpeg'],
    label_visibility="collapsed",
    key="file_uploader"
)

# Create a custom styled button to trigger the file uploader
if st.button(
    """
    <div class='upload-icon'>📁</div>
    <div class='upload-title'>رفع التمرين</div>
    <div class='upload-subtitle'>انقر هنا لرفع صورة من هاتفك</div>
    <div class='upload-hint'>الصور المدعومة: PNG, JPG, JPEG</div>
    """,
    key="custom_upload_button",
    use_container_width=True,
    type="primary",
    args=("custom-upload-button",)
):
    st.markdown("""
    <script>
    function triggerFileUpload() {
        let fileInput = document.querySelector('input[type="file"]') ||
                        document.querySelector('div[data-testid="stFileUploader"] input[type="file"]');
        if (fileInput) {
            console.log('File input found:', fileInput);
            fileInput.click();
        } else {
            console.error('File input not found!');
            alert('تعذر العثور على عنصر رفع الملف. تأكد من تحميل الصفحة بشكل كامل.');
        }
    }
    triggerFileUpload();
    </script>
    """, unsafe_allow_html=True)

# Show selected file info
if uploaded_file is not None:
    st.markdown(f"""
    <div class="file-info-card">
        <div style="font-family: 'Cairo', sans-serif; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">✅</div>
            <div style="color: #1a73e8; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">تم رفع الملف بنجاح!</div>
            <div style="color: #5f6368; font-size: 0.95rem;">{uploaded_file.name}</div>
            <div style="color: #9aa0a6; font-size: 0.8rem; margin-top: 0.5rem;">حجم الملف: {uploaded_file.size / 1024 / 1024:.1f} MB</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    # Solve button - mobile style
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
                    
                    # Solution in a nice card
                    st.markdown(f"""
                    <div style='
                        background: white;
                        border-radius: 20px;
                        padding: 2rem;
                        margin: 1rem 0;
                        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                        font-family: "Cairo", sans-serif;
                        line-height: 1.7;
                    '>
                        {response.text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(get_error_html(f"خطأ في التحليل: {str(e)}"), unsafe_allow_html=True)
                    st.info("📱 تأكد من جودة الصورة ووضوح النص")

# Footer
st.markdown(get_footer_html(), unsafe_allow_html=True)