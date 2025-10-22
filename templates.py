def get_header_html():
    """Return the header HTML"""
    return """
    <div style='text-align: center;'>
        <h1>🧪 اشرحلي</h1>
        <p>قم برفع صورة تمرين من مستوى الباكالوريا واحصل على حلول مفصلة خطوة بخطوة!</p>
    </div>
    """

def get_footer_html():
    """Return the footer HTML"""
    return """
    <div style='text-align: center; color: gray;'>
      For educational prupose we use streamlit and gemini
    </div>
    """

def get_success_html():
    """Return success message HTML"""
    return """
    <div style='text-align: center; color: green; font-weight: bold;'>
        ✅ تم إنشاء الحل!
    </div>
    """

def get_error_html(message):
    """Return error message HTML"""
    return f"""
    <div style='text-align: center; color: red; font-weight: bold;'>
        ❌ {message}
    </div>
    """



def get_success_html():
    """Return success message HTML"""
    return """
    <div style='text-align: center; color: green; font-weight: bold;'>
        ✅ تم إنشاء الحل!
    </div>
    """

def get_error_html(message):
    """Return error message HTML"""
    return f"""
    <div style='text-align: center; color: red; font-weight: bold;'>
        ❌ {message}
    </div>
    """