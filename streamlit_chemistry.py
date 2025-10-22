import streamlit as st
from PIL import Image
from config import configure_gemini, get_gemini_model
from templates import get_header_html, get_footer_html, get_success_html, get_error_html
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

# Simple file uploader for now
uploaded_file = st.file_uploader(
    "📤 رفع صورة التمرين",
    type=['png', 'jpg', 'jpeg'],
    help="📸 انقر لاختيار صورة من هاتفك"
)

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 الصورة المرفوعة", use_container_width=True)
    
    # Solve button
    if st.button("🚀 حل التمرين", type="primary"):
        if not st.session_state.api_configured:
            st.markdown(get_error_html("API not configured. Please check your settings."), unsafe_allow_html=True)
        else:
            with st.spinner("🔬 نقوم بتحليل التمرين... قد يستغرق هذا من 10 الى 20 ثانية"):
                try:
                    # Use Gemini model from config
                    model = get_gemini_model()
                    
                    # Use the imported prompt
                    response = model.generate_content([CHEMISTRY_PROMPT, image])
                    
                    # Display solution
                    st.markdown(get_success_html(), unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.markdown(get_error_html(f"Error analyzing image: {str(e)}"), unsafe_allow_html=True)
                    st.info("💡 نصائح: تأكد من أن الصورة واضحة وتحتوي على نص مقروء")

# Footer using HTML template
st.markdown("---")
st.markdown(get_footer_html(), unsafe_allow_html=True)