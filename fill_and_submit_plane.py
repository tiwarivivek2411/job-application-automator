import subprocess, json, base64, time

with open('/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf', 'rb') as f:
    pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

js_code = f"""
(function() {{
    var res = {{}};

    // 1. Attach Resume via DataTransfer
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

        var fileInput = document.getElementById("_systemfield_resume") || document.querySelector("input[type='file']");
        if (fileInput) {{
            var dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;
            fileInput.dispatchEvent(new Event("change", {{ bubbles: true }}));
            fileInput.dispatchEvent(new Event("input", {{ bubbles: true }}));
            res['resume'] = "ATTACHED: " + fileInput.files[0].name;
        }} else {{
            res['resume'] = "NO_FILE_INPUT";
        }}
    }} catch (e) {{
        res['resume'] = "ERROR: " + e.message;
    }}

    // Helper for React inputs
    function setReactValue(el, val) {{
        if (!el) return false;
        var proto = el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
        var setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        return true;
    }}

    // 2. Set all form fields
    res['name'] = setReactValue(document.getElementById('_systemfield_name'), 'Nilesh Tiwari');
    res['email'] = setReactValue(document.getElementById('_systemfield_email'), 'tiwarivivek2411@gmail.com');
    res['linkedin'] = setReactValue(document.getElementById('c5fb87a0-85f3-4c32-abe6-1324edb7559f'), 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    res['github'] = setReactValue(document.getElementById('a0da50ac-624f-48b1-bff0-b7272427edb0'), 'https://github.com/nileshtiwari');
    res['source'] = setReactValue(document.getElementById('55c24437-d543-4d32-9653-c28e04fd9bc8'), 'Open-source community and GitHub trending repositories');
    res['location'] = setReactValue(document.getElementById('8e799a7c-d4d9-44df-842b-d5d91fef2fbb'), 'Bengaluru, India');
    res['relocate'] = setReactValue(document.getElementById('588a2b1b-c645-477c-9833-07746a3c29fd'), 'Yes, open to relocation');
    res['join_date'] = setReactValue(document.getElementById('2e7db0c7-af7e-4e15-a428-31dea39ed68a'), 'Immediate / 15 Days');
    res['last_day'] = setReactValue(document.getElementById('5e420594-fc4c-44f8-ab23-d78d549e7dc1'), 'Feb 2026');
    res['current_ctc'] = setReactValue(document.getElementById('ed9a8c69-d641-489f-8ad4-0598003ba668'), '35 LPA');
    res['total_exp'] = setReactValue(document.getElementById('bb5dfd3a-aaa5-4f22-b5ef-dc5e9498be1a'), '4.5 Years');

    return JSON.stringify(res);
}})()
"""

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
print("FILL PLANE FORM OUT:\n", out.strip())
