def get_header_html():
    """Return the header HTML"""
    return """
    <div style='
        text-align: center; 
        font-family: "Cairo", sans-serif;
        padding: 1rem 0.5rem;
    '>
        <h1 style='
            font-family: "Cairo", sans-serif; 
            margin: 0.5rem 0; 
            color: #1a73e8;
            font-size: 1.8rem;
        '>🧪 اشرحلي</h1>
        <p style='
            font-family: "Cairo", sans-serif; 
            color: #5f6368;
            margin: 0;
            font-size: 1rem;
        '>ارفع صورة تمرين الباكالوريا واحصل على الحل</p>
    </div>
    """

def get_footer_html():
    """Return the footer HTML"""
    return """
    <div style='
        text-align: center; 
        color: #9aa0a6; 
        font-family: "Cairo", sans-serif;
        padding: 1.5rem 0.5rem;
        font-size: 0.8rem;
        border-top: 1px solid #e8eaed;
        margin-top: 2rem;
    '>
      تعليمي - Streamlit & Gemini
    </div>
    """

def get_success_html():
    """Return success message HTML"""
    return """
    <div style='
        background: #e6f4ea;
        color: #137333;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #34a853;
        font-family: "Cairo", sans-serif;
        text-align: center;
        font-weight: 600;
    '>
        ✅ تم إنشاء الحل بنجاح
    </div>
    """

def get_error_html(message):
    """Return error message HTML"""
    return f"""
    <div style='
        background: #fce8e6;
        color: #c5221f;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #ea4335;
        font-family: "Cairo", sans-serif;
        text-align: center;
        font-weight: 600;
    '>
        ❌ {message}
    </div>
    """