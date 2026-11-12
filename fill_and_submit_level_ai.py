import subprocess, json, base64, time

with open('/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf', 'rb') as f:
    pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

js_code = f"""
(function() {{
    var res = {{}};

    // 1. Attach Resume PDF
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
        if (fileInput) {{
            var dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;
            fileInput.dispatchEvent(new Event("change", {{ bubbles: true }}));
            fileInput.dispatchEvent(new Event("input", {{ bubbles: true }}));
            res['resume_attach'] = "SUCCESS: " + fileInput.files[0].name;
        }} else {{
            res['resume_attach'] = "NO_INPUT";
        }}
    }} catch(e) {{
        res['resume_attach'] = "ERROR: " + e.message;
    }}

    function setReactValue(el, val) {{
        if (!el) return false;
        var proto = el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
        var setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        return true;
    }}

    res['name'] = setReactValue(document.getElementById('_systemfield_name'), 'Nilesh Tiwari');
    res['email'] = setReactValue(document.getElementById('_systemfield_email'), 'tiwarivivek2411@gmail.com');
    res['company'] = setReactValue(document.getElementById('currentCompany'), 'Findem');
    res['location'] = setReactValue(document.getElementById('currentLocation'), 'Bengaluru, Karnataka, India');
    res['phone'] = setReactValue(document.getElementById('phone'), '+91 8920952855');
    res['linkedin'] = setReactValue(document.getElementById('LinkedIn'), 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    res['github'] = setReactValue(document.getElementById('GitHub'), 'https://github.com/nileshtiwari');
    
    var pitch = "4.5+ years of software engineering experience specializing in distributed backend systems, microservices, and cloud infrastructure using Java, Spring Boot, Python, AWS, Kafka, and Kubernetes. B.E. Computer Science from BITS Pilani (Hyderabad). Current CTC: 35 LPA, Expected CTC: 42 LPA, Notice Period: Immediate / 15 Days.";
    res['additional'] = setReactValue(document.getElementById('additionalInformation'), pitch);

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
print("FILL LEVEL AI OUT:\n", out.strip())

time.sleep(2)

# Check submit button and submit
submit_js = """
(function() {
    var btn = Array.from(document.querySelectorAll("button")).find(b => b.innerText && b.innerText.includes("Submit Application"));
    if (btn && !btn.disabled) {
        btn.click();
        return "CLICKED_SUBMIT";
    }
    return "CANNOT_SUBMIT: " + (btn ? ("disabled=" + btn.disabled) : "not found");
})()
"""
escaped_sub = submit_js.replace('\n', ' ').replace('"', '\\"')
ascript_sub = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{escaped_sub}")
    end tell
end tell
'''
p2 = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out2, err2 = p2.communicate(ascript_sub)
print("SUBMIT ACTION:", out2.strip())
