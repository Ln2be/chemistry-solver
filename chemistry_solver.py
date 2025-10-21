from flask import Flask, request, jsonify
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)

# HTML template as a string
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chemistry Problem Solver</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f0f2f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        .input-group {
            margin: 20px 0;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #2c3e50;
        }
        input[type="password"], input[type="file"] {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 15px;
            box-sizing: border-box;
        }
        button {
            background: #3498db;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            margin-top: 10px;
        }
        button:hover {
            background: #2980b9;
        }
        button:disabled {
            background: #bdc3c7;
            cursor: not-allowed;
        }
        #result {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            display: none;
        }
        .loading {
            color: #7f8c8d;
            text-align: center;
            font-style: italic;
        }
        .solution-content {
            white-space: pre-line;
            line-height: 1.6;
        }
        .info-box {
            background: #e8f4fd;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            border-left: 4px solid #3498db;
        }
        .success {
            color: #27ae60;
        }
        .error {
            color: #e74c3c;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Chemistry Problem Solver</h1>
        <p>Upload an image of a high school chemistry problem and get detailed step-by-step solutions!</p>
        
        <div class="info-box">
            <strong>Get your free API key:</strong> 
            <a href="https://aistudio.google.com/" target="_blank">https://aistudio.google.com/</a>
        </div>
        
        <div class="input-group">
            <label for="apiKey">Google Gemini API Key:</label>
            <input type="password" id="apiKey" placeholder="Enter your API key from Google AI Studio">
        </div>
        
        <div class="input-group">
            <label for="imageUpload">Chemistry Problem Image:</label>
            <input type="file" id="imageUpload" accept="image/*">
        </div>
        
        <button onclick="solveProblem()" id="solveBtn">Solve Chemistry Problem</button>
        
        <div id="result">
            <h3>🧪 Solution:</h3>
            <div id="solution" class="solution-content"></div>
        </div>
    </div>

    <script>
        async function solveProblem() {
            const apiKey = document.getElementById('apiKey').value;
            const fileInput = document.getElementById('imageUpload');
            const resultDiv = document.getElementById('result');
            const solutionDiv = document.getElementById('solution');
            const solveBtn = document.getElementById('solveBtn');
            
            if (!apiKey) {
                alert('Please enter your Gemini API key');
                return;
            }
            
            if (!fileInput.files[0]) {
                alert('Please select an image file');
                return;
            }

            // Disable button and show loading
            solveBtn.disabled = true;
            solveBtn.textContent = 'Analyzing Problem...';
            solutionDiv.innerHTML = '<div class="loading">Analyzing chemistry problem... This may take a few seconds.</div>';
            resultDiv.style.display = 'block';

            const formData = new FormData();
            formData.append('api_key', apiKey);
            formData.append('image', fileInput.files[0]);

            try {
                const response = await fetch('/solve', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Format the solution with better styling
                    const formattedSolution = data.solution
                        .replace(/\\n/g, '<br>')
                        .replace(/PROBLEM UNDERSTANDING:/g, '<strong class="success">🔍 PROBLEM UNDERSTANDING:</strong>')
                        .replace(/RELEVANT CONCEPTS:/g, '<strong class="success">🧠 RELEVANT CONCEPTS:</strong>')
                        .replace(/STEP-BY-STEP SOLUTION:/g, '<strong class="success">📝 STEP-BY-STEP SOLUTION:</strong>')
                        .replace(/FINAL ANSWER:/g, '<strong class="success">✅ FINAL ANSWER:</strong>')
                        .replace(/KEY LEARNING POINTS:/g, '<strong class="success">💡 KEY LEARNING POINTS:</strong>');
                    
                    solutionDiv.innerHTML = formattedSolution;
                } else {
                    solutionDiv.innerHTML = '<div class="error">Error: ' + data.error + '</div>';
                }
                
            } catch (error) {
                solutionDiv.innerHTML = '<div class="error">Network error: ' + error + '</div>';
            } finally {
                // Re-enable button
                solveBtn.disabled = false;
                solveBtn.textContent = 'Solve Chemistry Problem';
            }
        }
        
        // Allow pressing Enter in API key field to solve
        document.getElementById('apiKey').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                solveProblem();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML

@app.route('/solve', methods=['POST'])
def solve():
    try:
        api_key = request.form['api_key']
        image_file = request.files['image']
        
        if not api_key:
            return jsonify({'success': False, 'error': 'API key is required'})
        
        if not image_file:
            return jsonify({'success': False, 'error': 'Image is required'})
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Use the correct Gemini 2.0 model
        model = genai.GenerativeModel('models/gemini-2.0-flash-001')
        
        # Open image
        image = Image.open(image_file.stream)
        
        # Analyze chemistry problem
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
        Use clear, simple language and explain each step thoroughly.
        """
        
        response = model.generate_content([prompt, image])
        
        return jsonify({
            'success': True,
            'solution': response.text
        })
        
    except Exception as e:
        error_msg = str(e)
        # Provide more user-friendly error messages
        if "404" in error_msg:
            return jsonify({
                'success': False,
                'error': 'Model not found. Please try again later.'
            })
        elif "403" in error_msg:
            return jsonify({
                'success': False,
                'error': 'Invalid API key or permission denied. Please check your API key.'
            })
        elif "429" in error_msg:
            return jsonify({
                'success': False,
                'error': 'Rate limit exceeded. Please wait a moment and try again.'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Error: {error_msg}'
            })

if __name__ == '__main__':
    print("🧪 Chemistry Solver App Starting...")
    print("🌐 Open your web browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)