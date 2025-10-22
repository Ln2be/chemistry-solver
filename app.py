import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# Set page config - MUST BE FIRST
st.set_page_config(
    page_title="Chemistry Problem Solver",
    page_icon="🧪",
    layout="centered"
)

# App title and description
st.title("🧪 Chemistry Problem Solver")
st.markdown("Upload an image of a high school chemistry problem and get detailed step-by-step solutions!")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    .solution-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #27ae60;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_configured' not in st.session_state:
    st.session_state.api_configured = False

# Configure Gemini - Hugging Face uses environment variables
try:
    # Get API key from Hugging Face secrets
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
        st.session_state.api_configured = True
        st.success("✅ API configured successfully!")
    else:
        st.error("❌ API key not found. Please add GEMINI_API_KEY to your Hugging Face secrets.")
except Exception as e:
    st.error(f"❌ Error configuring Gemini: {str(e)}")

# Info section
with st.container():
    st.markdown("""
    <div class="info-box">
        <h3>✨ How to Use</h3>
        <ol>
            <li>Take a picture or upload an image of your chemistry problem</li>
            <li>Click 'Solve Chemistry Problem'</li>
            <li>Get detailed, step-by-step explanations instantly!</li>
        </ol>
        <p><strong>Supported topics:</strong> Stoichiometry, Balancing Equations, Molar Mass, Gas Laws, Solutions, Thermochemistry, and more!</p>
    </div>
    """, unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "📤 Upload Chemistry Problem Image",
    type=['png', 'jpg', 'jpeg'],
    help="Upload a clear image of your chemistry problem"
)

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Chemistry Problem", use_column_width=True)
    
    # Analyze button
    if st.button("🚀 Solve Chemistry Problem", type="primary"):
        if not st.session_state.api_configured:
            st.error("API not configured. Please check your settings.")
        else:
            with st.spinner("🔬 Analyzing your chemistry problem... This may take 10-20 seconds."):
                try:
                    # Use Gemini model
                    model = genai.GenerativeModel('models/gemini-2.0-flash-001')
                    
                    # Create prompt for chemistry problem
                    prompt = """
                    You are an expert high school chemistry tutor. Analyze this chemistry problem image and provide a comprehensive, educational solution.
                    
                    Please structure your response as follows:
                    
                    PROBLEM UNDERSTANDING:
                    Briefly explain what the problem is asking.
                    
                    RELEVANT CONCEPTS: 
                    List the key chemistry concepts needed to solve this problem.
                    
                    STEP-BY-STEP SOLUTION:
                    Provide a detailed, step-by-step solution with clear explanations for each step.
                    
                    FINAL ANSWER:
                    Clearly state the final answer with proper units.
                    
                    KEY LEARNING POINTS:
                    Summarize the main takeaways and common pitfalls.
                    
                    Make the explanation beginner-friendly and educational for high school students.
                    """
                    
                    # Generate response
                    response = model.generate_content([prompt, image])
                    
                    # Display solution
                    st.success("✅ Solution Generated!")
                    st.markdown("---")
                    st.markdown('<div class="solution-box">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error analyzing image: {str(e)}")
                    st.info("💡 Tips: Make sure the image is clear and contains readable text.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Built with Streamlit and Google Gemini • For educational purposes"
    "</div>",
    unsafe_allow_html=True
)
