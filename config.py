import google.generativeai as genai
import streamlit as st

def configure_gemini():
    """Configure Gemini AI model and settings"""
    try:
        if 'GEMINI_API_KEY' in st.secrets:
            api_key = st.secrets['GEMINI_API_KEY']
            genai.configure(api_key=api_key)
            st.session_state.api_configured = True
            return True
        else:
            st.error("❌ API key not found in secrets. Please add GEMINI_API_KEY to your Streamlit secrets.")
            return False
    except Exception as e:
        st.error(f"❌ Error configuring Gemini: {str(e)}")
        return False

def get_gemini_model():
    """Get the configured Gemini model"""
    return genai.GenerativeModel('models/gemini-2.0-flash-001')