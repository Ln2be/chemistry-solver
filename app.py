import gradio as gr
import google.generativeai as genai
from PIL import Image
import os

# Configure Gemini
api_key = os.environ.get('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.0-flash-001')
else:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

def solve_chemistry_problem(image):
    """Analyze chemistry problem image and return solution"""
    if image is None:
        return "⚠️ Please upload an image first."
    
    try:
        # Create prompt for chemistry problem
        prompt = """
        You are an expert high school chemistry tutor. Analyze this chemistry problem image and provide a comprehensive, educational solution.
        
        Please structure your response as follows:
        
        🧪 PROBLEM UNDERSTANDING:
        Briefly explain what the problem is asking.
        
        📚 RELEVANT CONCEPTS: 
        List the key chemistry concepts needed to solve this problem.
        
        🔬 STEP-BY-STEP SOLUTION:
        Provide a detailed, step-by-step solution with clear explanations for each step.
        
        ✅ FINAL ANSWER:
        Clearly state the final answer with proper units.
        
        💡 KEY LEARNING POINTS:
        Summarize the main takeaways and common pitfalls.
        
        Make the explanation beginner-friendly and educational for high school students.
        Use clear section headers and bullet points for better readability.
        """
        
        # Generate response
        response = model.generate_content([prompt, image])
        return response.text
        
    except Exception as e:
        return f"❌ Error analyzing image: {str(e)}\n\n💡 Tips: Make sure the image is clear, well-lit, and contains readable text."

# Custom CSS for better styling
custom_css = """
#title { text-align: center; }
.contain { max-width: 1200px; margin: 0 auto; }
"""

# Create Gradio interface
with gr.Blocks(
    theme=gr.themes.Soft(),
    title="Chemistry Problem Solver",
    css=custom_css
) as demo:
    
    gr.Markdown(
        """
        # 🧪 Chemistry Problem Solver
        ### Upload an image of a high school chemistry problem and get detailed step-by-step solutions!
        
        **Supported topics:** Stoichiometry • Balancing Equations • Molar Mass • Gas Laws • Solutions • Thermochemistry • Acid-Base Reactions
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📤 Upload Your Problem")
            image_input = gr.Image(
                type="pil",
                label="Chemistry Problem Image",
                height=300,
                sources=["upload", "webcam"],
                help="Take a picture or upload an image of your chemistry problem"
            )
            
            with gr.Row():
                clear_btn = gr.Button("🔄 Clear", size="sm")
                solve_btn = gr.Button("🚀 Solve Chemistry Problem", variant="primary", scale=2)
            
            gr.Markdown(
                """
                ### 💡 How to Use:
                1. **Upload** an image of your chemistry problem
                2. **Click** "Solve Chemistry Problem" 
                3. **Get** detailed step-by-step solution
                
                *For best results, ensure the image is clear and text is readable*
                """
            )
        
        with gr.Column(scale=2):
            gr.Markdown("### 🎯 Solution")
            solution_output = gr.Markdown(
                label="Step-by-Step Solution",
                value="*Your solution will appear here after analysis...*"
            )
    
    # Button actions
    solve_btn.click(
        fn=solve_chemistry_problem,
        inputs=image_input,
        outputs=solution_output,
        api_name="solve"
    )
    
    clear_btn.click(
        fn=lambda: (None, "*Solution cleared*"),
        inputs=[],
        outputs=[image_input, solution_output]
    )
    
    # Footer
    gr.Markdown("---")
    gr.Markdown(
        "<div style='text-align: center; color: gray;'>"
        "Built with Gradio and Google Gemini • For educational purposes"
        "</div>"
    )

# Launch the app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
