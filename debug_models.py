import google.generativeai as genai
import sys

# Replace with your actual API key
API_KEY = "AIzaSyB7iSryZL_AlR_tV9l6L9Am7vHB1f6m7Zw"  # Put your real key here

def debug_gemini():
    print("🔍 Starting Gemini Debug...")
    print(f"Python version: {sys.version}")
    
    try:
        # Test 1: Basic configuration
        print("\n1. Testing API configuration...")
        genai.configure(api_key=API_KEY)
        print("✅ API configuration successful")
        
        # Test 2: List available models
        print("\n2. Listing available models...")
        models = genai.list_models()
        
        gemini_models = []
        for model in models:
            if 'gemini' in model.name.lower():
                gemini_models.append(model)
                print(f"📋 Found: {model.name}")
                print(f"   Display: {model.display_name}")
                print(f"   Methods: {model.supported_generation_methods}")
                print()
        
        if not gemini_models:
            print("❌ No Gemini models found!")
            return
        
        # Test 3: Try to use a model
        print("\n3. Testing model generation...")
        
        # Try common model names
        test_models = [
            'gemini-1.5-pro',
            'gemini-1.5-flash', 
            'gemini-pro',
            'gemini-1.0-pro',
        ]
        
        for model_name in test_models:
            print(f"\nTesting: {model_name}")
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say 'Hello World' in 2 words.")
                print(f"✅ {model_name}: SUCCESS - '{response.text.strip()}'")
            except Exception as e:
                print(f"❌ {model_name}: FAILED - {str(e)[:100]}")
                
    except Exception as e:
        print(f"💥 Major error: {e}")

if __name__ == "__main__":
    if API_KEY == "YOUR_API_KEY_HERE":
        print("❌ Please replace API_KEY with your actual Gemini API key")
    else:
        debug_gemini()