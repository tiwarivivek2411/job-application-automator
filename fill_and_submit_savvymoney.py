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
    res['phone'] = setReactValue(document.getElementById('fb6dc58a-cecc-4dae-80ba-53a117d1c4bd'), '+91 8920952855');
    res['zip'] = setReactValue(document.getElementById('af1ff5dd-e3d4-4072-a320-15b53517e6a1'), '560037');
    res['pay'] = setReactValue(document.getElementById('e330b627-d26b-4469-8f44-c1153ee4087e'), '42 LPA');
    res['portfolio'] = setReactValue(document.getElementById('6f3499e7-bc30-43e3-aced-c634610e643e'), 'https://github.com/nileshtiwari');
    res['linkedin'] = setReactValue(document.getElementById('9578069f-f854-401a-a031-c0a84629efac'), 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    res['college'] = setReactValue(document.getElementById('62abf8d5-352c-4938-98ba-a1b6f1e6117a'), 'BITS Pilani');
    res['referral'] = setReactValue(document.getElementById('b9dc0089-7477-443e-8d6a-25618c3e9d5e'), 'Job Board / Online');
    res['notice_period'] = setReactValue(document.getElementById('56cc2422-f5e7-4ea1-8625-951c22fcc24a'), '15 Days / Immediate');

    // Date available
    var dateInput = document.querySelector(".react-datepicker__input-container input");
    if (dateInput) {{
        setReactValue(dateInput, "11/15/2026");
        res['date'] = true;
    }}

    // City autocomplete
    var cityField = document.querySelector("[data-field-path=\\"_systemfield_location\\"]");
    var cityInput = cityField ? cityField.querySelector("input") : null;
    if (cityInput) {{
        cityInput.focus();
        cityInput.value = "Bengaluru";
        cityInput.dispatchEvent(new Event("input", {{ bubbles: true }}));
        res['city_typed'] = true;
    }}

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
print("FILL STEP 1 OUT:\n", out.strip())

time.sleep(1.5)

# Step 2: Click City option from listbox
select_city_js = """
(function() {
    var option = Array.from(document.querySelectorAll("[role='option'], li")).find(o => o.innerText.includes("Bengaluru"));
    if (option) {
        option.click();
        return "CLICKED_CITY_OPTION: " + option.innerText.trim();
    }
    return "NO_CITY_OPTION";
})()
"""
b64_city = base64.b64encode(select_city_js.encode('utf-8')).decode('utf-8')
ascript_city = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "eval(atob('{b64_city}'))")
    end tell
end tell
'''
p2 = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out2, err2 = p2.communicate(ascript_city)
print("CITY OPTION:", out2.strip())

time.sleep(1.0)

# Step 3: Highest Education
edu_js = """
(function() {
    var eduField = Array.from(document.querySelectorAll("fieldset, div")).find(f => f.innerText && f.innerText.includes("Highest Education"));
    var btn = eduField ? eduField.querySelector("button") : null;
    if (btn) btn.click();
    return "CLICKED_EDU_TOGGLE";
})()
"""
b64_edu = base64.b64encode(edu_js.encode('utf-8')).decode('utf-8')
ascript_edu = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "eval(atob('{b64_edu}'))")
    end tell
end tell
'''
p3 = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out3, err3 = p3.communicate(ascript_edu)
print("EDU TOGGLE:", out3.strip())

time.sleep(1.0)

# Check Education options
edu_options_js = """
(function() {
    var options = Array.from(document.querySelectorAll("[role='option'], li")).map(o => o.innerText.trim()).filter(t => t.length > 0);
    return JSON.stringify(options);
})()
"""
b64_opts = base64.b64encode(edu_options_js.encode('utf-8')).decode('utf-8')
ascript_opts = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "eval(atob('{b64_opts}'))")
    end tell
end tell
'''
p4 = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out4, err4 = p4.communicate(ascript_opts)
print("EDU OPTIONS:", out4.strip())
