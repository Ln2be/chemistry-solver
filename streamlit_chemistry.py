import streamlit as st
from PIL import Image
from config import configure_gemini, get_gemini_model
from templates import get_header_html, get_footer_html, get_success_html, get_error_html, get_upload_section_html
from prompts import CHEMISTRY_PROMPT

# Mobile app styling
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
    .main {
        padding: 0 1rem;
    }
    .stFileUploader > div > div {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
    }
    .stFileUploader > label {
        display: none !important;
    }
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-family: "Cairo", sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        background: #1a73e8;
    }
    .stButton > button:hover {
        background: #1669c1;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
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

# Hidden file uploader that uses the beautiful section as trigger
uploaded_file = st.file_uploader(
    "رفع صورة التمرين",
    type=['png', 'jpg', 'jpeg'],
    label_visibility="collapsed"
)

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
                    '>
                        {response.text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(get_error_html(f"خطأ في التحليل: {str(e)}"), unsafe_allow_html=True)
                    st.info("📱 تأكد من جودة الصورة ووضوح النص")

# Footer
st.markdown(get_footer_html(), unsafe_allow_html=True)