import subprocess, json, pypdf

# 1. Read full PDF resume text
reader = pypdf.PdfReader('/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf')
full_resume = ''
for page in reader.pages:
    full_resume += (page.extract_text() or '') + '\n'

escaped_resume = full_resume.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

js_code = f"""
(function() {{
    var ta = document.getElementById('resume_text');
    if (ta) {{
        ta.value = "{escaped_resume}";
        ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
        ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
        return "RESUME_PASTED_SUCCESS: " + ta.value.length + " chars";
    }}
    return "NO_TEXTAREA";
}})()
"""

cleaned_lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
escaped = ' '.join(cleaned_lines).replace('\\', '\\\\').replace('"', '\\"')

ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{escaped}")
    end tell
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("INJECT RESUME RESULT:", out)
if err: print("ERR:", err)
