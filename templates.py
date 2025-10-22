def get_header_html():
    """Return the header HTML"""
    return """
    <div style='
        text-align: center; 
        font-family: "Cairo", sans-serif;
    '>
        <h1 style='font-family: "Cairo", sans-serif;'>🧪 اشرحلي</h1>
        <p style='font-family: "Cairo", sans-serif;'>قم برفع صورة تمرين من مستوى الباكالوريا واحصل على حلول مفصلة خطوة بخطوة!</p>
    </div>
    """

def get_footer_html():
    """Return the footer HTML"""
    return """
    <div style='
        text-align: center; 
        color: gray; 
        font-family: "Cairo", sans-serif;
    '>
      For educational purpose we use streamlit and gemini
    </div>
    """

def get_success_html():
    """Return success message HTML"""
    return """
    <div style='
        text-align: center; 
        color: green; 
        font-weight: bold;
        font-family: "Cairo", sans-serif;
    '>
        ✅ تم إنشاء الحل!
    </div>
    """

def get_error_html(message):
    """Return error message HTML"""
    return f"""
    <div style='
        text-align: center; 
        color: red; 
        font-weight: bold;
        font-family: "Cairo", sans-serif;
    '>
        ❌ {message}
    </div>
    """