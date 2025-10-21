from flask import Flask, request, jsonify
import google.generativeai as genai
from PIL import Image
import io
from prompts import CHEMISTRY_PROMPT  # Import our custom prompt
from config import GEMINI_API_KEY, APP_CONFIG  # Import API key and config

app = Flask(__name__)

# Configure Gemini with the embedded API key
try:
    genai.configure(api_key=GEMINI_API_KEY)
    API_KEY_VALID = True
except Exception as e:
    print(f"❌ API Key Error: {e}")
    API_KEY_VALID = False

# HTML template as a string
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chemistry Problem Solver</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-top: 20px;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
        }
        .input-group {
            margin: 25px 0;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #2c3e50;
        }
        input[type="file"] {
            width: 100%;
            padding: 12px;
            border: 2px dashed #3498db;
            border-radius: 8px;
            margin-bottom: 15px;
            box-sizing: border-box;
            background: #f8f9fa;
        }
        button {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            margin-top: 10px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        button:disabled {
            background: #bdc3c7;
            transform: none;
            box-shadow: none;
            cursor: not-allowed;
        }
        #result {
            margin-top: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
            display: none;
            border-left: 5px solid #3498db;
        }
        .loading {
            color: #7f8c8d;
            text-align: center;
            font-style: italic;
            padding: 20px;
        }
        .solution-content {
            white-space: pre-line;
            line-height: 1.7;
            font-size: 15px;
        }
        .info-box {
            background: #e8f4fd;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }
        .success {
            color: #27ae60;
            font-weight: bold;
        }
        .error {
            color: #e74c3c;
            background: #ffeaea;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
        }
        .section-title {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
            margin-top: 25px;
        }
        .api-status {
            text-align: center;
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
            font-weight: bold;
        }
        .api-valid {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .api-invalid {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Chemistry Problem Solver</h1>
        <div class="subtitle">Upload an image of any chemistry problem and get instant step-by-step solutions!</div>
        
        <div id="apiStatus" class="api-status"></div>
        
        <div class="info-box">
            <strong>✨ How to use:</strong> 
            <ol>
                <li>Take a picture or upload an image of your chemistry problem</li>
                <li>Click "Solve Chemistry Problem"</li>
                <li>Get detailed, step-by-step explanations</li>
            </ol>
            <p><strong>Supported topics:</strong> Stoichiometry, Balancing Equations, Molar Mass, Gas Laws, Solutions, Thermochemistry, and more!</p>
        </div>
        
        <div class="input-group">
            <label for="imageUpload">📤 Upload Chemistry Problem Image:</label>
            <input type="file" id="imageUpload" accept="image/*">
            <small>Supported formats: PNG, JPG, JPEG (Max 10MB)</small>
        </div>
        
        <button onclick="solveProblem()" id="solveBtn">🚀 Solve Chemistry Problem</button>
        
        <div id="result">
            <h3 class="section-title">🎯 Solution</h3>
            <div id="solution" class="solution-content"></div>
        </div>
    </div>

    <script>
        // Update API status
        function updateApiStatus() {
            const statusDiv = document.getElementById('apiStatus');
            statusDiv.className = 'api-status api-valid';
            statusDiv.innerHTML = '✅ API Connected - Ready to solve chemistry problems!';
        }
        
        // Call on page load
        window.onload = updateApiStatus;
        
        async function solveProblem() {
            const fileInput = document.getElementById('imageUpload');
            const resultDiv = document.getElementById('result');
            const solutionDiv = document.getElementById('solution');
            const solveBtn = document.getElementById('solveBtn');
            
            if (!fileInput.files[0]) {
                alert('Please select an image file containing a chemistry problem');
                return;
            }

            // Disable button and show loading
            solveBtn.disabled = true;
            solveBtn.textContent = '🔬 Analyzing Chemistry Problem...';
            solutionDiv.innerHTML = '<div class="loading">Analyzing your chemistry problem... This may take 10-20 seconds.</div>';
            resultDiv.style.display = 'block';

            const formData = new FormData();
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
                        .replace(/🧪 PROBLEM ANALYSIS/g, '<div class="section-title">🧪 PROBLEM ANALYSIS</div>')
                        .replace(/📚 KEY CONCEPTS/g, '<div class="section-title">📚 KEY CONCEPTS</div>')
                        .replace(/🔬 STEP-BY-STEP SOLUTION/g, '<div class="section-title">🔬 STEP-BY-STEP SOLUTION</div>')
                        .replace(/✅ FINAL ANSWER/g, '<div class="section-title">✅ FINAL ANSWER</div>')
                        .replace(/💡 LEARNING TIPS/g, '<div class="section-title">💡 LEARNING TIPS</div>')
                        .replace(/- /g, '• ')
                        .replace(/\[Answer\]/g, '<div style="background: #e8f4fd; padding: 10px; border-radius: 5px; border-left: 4px solid #27ae60; margin: 10px 0;"><strong>Answer:</strong>');
                    
                    solutionDiv.innerHTML = formattedSolution;
                } else {
                    solutionDiv.innerHTML = '<div class="error">❌ ' + data.error + '</div>';
                }
                
            } catch (error) {
                solutionDiv.innerHTML = '<div class="error">❌ Network error: ' + error + '</div>';
            } finally {
                // Re-enable button
                solveBtn.disabled = false;
                solveBtn.textContent = '🚀 Solve Chemistry Problem';
            }
        }
        
        // Add some interactive effects
        document.getElementById('imageUpload').addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                this.style.borderColor = '#27ae60';
                this.style.background = '#f0fff4';
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
        # Check if API key is valid
        if not API_KEY_VALID:
            return jsonify({
                'success': False,
                'error': 'API configuration error. Please check the API key.'
            })
        
        image_file = request.files['image']
        
        if not image_file:
            return jsonify({'success': False, 'error': 'Please select an image file'})
        
        # Check file size (max 10MB)
        image_file.seek(0, 2)  # Seek to end
        file_size = image_file.tell()  # Get file size
        image_file.seek(0)  # Reset to beginning
        
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            return jsonify({'success': False, 'error': 'Image file too large. Maximum size is 10MB.'})
        
        # Use the configured model
        model = genai.GenerativeModel(APP_CONFIG["model_name"])
        
        # Open image
        image = Image.open(image_file.stream)
        
        # Use our custom prompt from prompts.py
        response = model.generate_content([CHEMISTRY_PROMPT, image])
        
        return jsonify({
            'success': True,
            'solution': response.text
        })
        
    except Exception as e:
        error_msg = str(e)
        # Provide user-friendly error messages
        if "404" in error_msg:
            return jsonify({
                'success': False,
                'error': 'Service temporarily unavailable. Please try again later.'
            })
        elif "403" in error_msg:
            return jsonify({
                'success': False,
                'error': 'API access denied. Please check the configuration.'
            })
        elif "429" in error_msg:
            return jsonify({
                'success': False,
                'error': 'Too many requests. Please wait a moment and try again.'
            })
        elif "503" in error_msg:
            return jsonify({
                'success': False,
                'error': 'Service temporarily unavailable. Please try again in a few minutes.'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Something went wrong: {error_msg}'
            })

if __name__ == '__main__':
    print("🧪 Advanced Chemistry Solver App Starting...")
    print("🌐 Open your web browser and go to: http://localhost:5000")
    print("🔑 API Key:", "✅ Configured" if API_KEY_VALID else "❌ Invalid")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)