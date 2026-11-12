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
    res['linkedin'] = setReactValue(document.getElementById('d8f45615-2a98-4dd4-be24-0a58ae600b0b'), 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');

    var pitch = "4.5+ years of software engineering experience specializing in distributed backend systems, microservices, and cloud infrastructure using Java, Spring Boot, Python, AWS, Kafka, and Kubernetes. B.E. Computer Science from BITS Pilani (Hyderabad). Current CTC: 35 LPA, Expected CTC: 42 LPA, Notice Period: Immediate / 15 Days.";
    res['comments'] = setReactValue(document.getElementById('50450afe-a496-48b3-816e-0bcdb87358d1'), pitch);

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
print("FILL BUILD AI OUT:\n", out.strip())

time.sleep(2)

# Submit
submit_js = """
(function() {
    var btn = document.querySelector(".ashby-application-form-submit-button");
    if (!btn) return "NO BTN";
    btn.scrollIntoView({ behavior: "smooth", block: "center" });
    btn.focus();
    btn.click();
    return "CLICKED_SUBMIT";
})()
"""
b64_sub = base64.b64encode(submit_js.encode('utf-8')).decode('utf-8')
ascript_sub = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "eval(atob('{b64_sub}'))")
    end tell
end tell
'''
p2 = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out2, err2 = p2.communicate(ascript_sub)
print("SUBMIT ACTION:", out2.strip())
