import subprocess, base64

# Read PDF bytes as base64
with open('/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf', 'rb') as f:
    pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

js_code = f"""
(function() {{
    try {{
        var b64Data = "{pdf_b64}";
        var byteCharacters = atob(b64Data);
        var byteNumbers = new Array(byteCharacters.length);
        for (var i = 0; i < byteCharacters.length; i++) {{
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }}
        var byteArray = new Uint8Array(byteNumbers);
        var blob = new Blob([byteArray], {{ type: "application/pdf" }});
        var file = new File([blob], "Resume-Nilesh-Tiwari-1302.pdf", {{ type: "application/pdf" }});

        var fileInput = document.getElementById("_systemfield_resume");
        if (!fileInput) return "NO_FILE_INPUT";

        var dt = new DataTransfer();
        dt.items.add(file);
        fileInput.files = dt.files;
        fileInput.dispatchEvent(new Event("change", {{ bubbles: true }}));
        fileInput.dispatchEvent(new Event("input", {{ bubbles: true }}));

        return "JS_FILE_ATTACH_SUCCESS: " + fileInput.files[0].name + " (" + fileInput.files[0].size + " bytes)";
    }} catch (e) {{
        return "ERROR: " + e.message;
    }}
}})()
"""

# Pass via base64 to avoid string escaping issues
ascript_payload = base64.b64encode(js_code.encode('utf-8')).decode('utf-8')

ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "eval(atob('{ascript_payload}'))")
    end tell
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("ATTACH OUT:", out.strip())
if err: print("ERR:", err)
