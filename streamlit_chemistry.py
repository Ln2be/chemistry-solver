import streamlit as st
from PIL import Image
from config import configure_gemini, get_gemini_model
from templates import get_header_html, get_footer_html, get_success_html, get_error_html, get_upload_section_html
from prompts import CHEMISTRY_PROMPT

# Mobile app styling with enhanced file uploader
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
    .main {
        padding: 0 1rem;
    }
    
    /* Hide the default file uploader appearance */
    .stFileUploader > div > div {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
    }
    
    .stFileUploader > label {
        display: none !important;
    }
    
    /* Style the "Browse files" button */
    .stFileUploader > div > div > button {
        width: 100% !important;
        border-radius: 16px !important;
        height: 60px !important;
        font-family: "Cairo", sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        border: none !important;
        background: linear-gradient(135deg, #1a73e8, #0d47a1) !important;
        color: white !important;
        margin-top: 1rem !important;
        box-shadow: 0 4px 20px rgba(26, 115, 232, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div > div > button:hover {
        background: linear-gradient(135deg, #1669c1, #0b3d91) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(26, 115, 232, 0.4) !important;
    }
    
    .stFileUploader > div > div > button:active {
        transform: translateY(0) !important;
    }
    
    /* Style the selected file name */
    .stFileUploader > div > div > div > div {
        font-family: "Cairo", sans-serif !important;
        text-align: center !important;
        margin-top: 0.5rem !important;
        color: #1a73e8 !important;
        font-weight: 600 !important;
    }
    
    /* Solve button styling */
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
        box-shadow: 0 4px 20px rgba(52, 168, 83, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2e8b47, #0d8040);
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(52, 168, 83, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
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

# Mobile-style upload section
st.markdown(get_upload_section_html(), unsafe_allow_html=True)

# Hidden file uploader with beautiful button
uploaded_file = st.file_uploader(
    "📁 اختر ملف الصورة",
    type=['png', 'jpg', 'jpeg'],
    label_visibility="collapsed"
)

# Add custom instruction below the uploader
if uploaded_file is None:
    st.markdown("""
    <div style='
        text-align: center; 
        color: #5f6368; 
        font-family: "Cairo", sans-serif;
        margin: 0.5rem 0 2rem 0;
        font-size: 0.9rem;
    '>
        انقر على الزر أعلاه لرفع صورة التمرين
    </div>
    """, unsafe_allow_html=True)

if uploaded_file is not None:
    # Display the uploaded image in a card
    image = Image.open(uploaded_file)
    st.markdown("""
    <div style='
        background: white;
        border-radius: 16px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    '>
    </div>
    """, unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    
    # Show file info
    st.markdown(f"""
    <div style='
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        font-family: "Cairo", sans-serif;
        color: #5f6368;
        border: 1px dashed #e8eaed;
    '>
        📄 <strong>تم رفع الملف:</strong> {uploaded_file.name}
    </div>
    """, unsafe_allow_html=True)
    
    # Solve button - mobile style
    if st.button("🚀 حل التمرين الآن", type="primary"):
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
                        border-radius: 16px;
                        padding: 1.5rem;
                        margin: 1rem 0;
                        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
                        font-family: "Cairo", sans-serif;
                        line-height: 1.6;
                    '>
                        {response.text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(get_error_html(f"خطأ في التحليل: {str(e)}"), unsafe_allow_html=True)
                    st.info("📱 تأكد من جودة الصورة ووضوح النص")

# Footer
st.markdown(get_footer_html(), unsafe_allow_html=True)