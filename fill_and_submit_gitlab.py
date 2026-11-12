import subprocess, json, base64, time

def run_js(js):
    b64 = base64.b64encode(js.encode('utf-8')).decode('utf-8')
    ascript = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684133)
            return (execute javascript "eval(atob('{b64}'))")
        end tell
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(ascript)
    return out.strip()

# 1. Attach Resume PDF
with open('/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf', 'rb') as f:
    pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

attach_js = f"""
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

        var fileInput = document.getElementById("resume");
        if (fileInput) {{
            var dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;
            fileInput.dispatchEvent(new Event("change", {{ bubbles: true }}));
            fileInput.dispatchEvent(new Event("input", {{ bubbles: true }}));
            return "ATTACHED: " + fileInput.files[0].name;
        }}
        return "NO_RESUME_INPUT";
    }} catch(e) {{
        return "ERROR: " + e.message;
    }}
}})()
"""
res_attach = run_js(attach_js)
print("ATTACH RES:", res_attach)

time.sleep(1.0)

# 2. Select Phone Country +91
country_phone_js = """
(function() {
    var itiBtn = document.querySelector(".iti__selected-country");
    if (itiBtn) itiBtn.click();
    
    var search = document.getElementById("iti-0__search-input") || document.querySelector(".iti__search-input");
    if (search) {
        search.focus();
        search.value = "India";
        search.dispatchEvent(new Event("input", { bubbles: true }));
    }
    
    var items = Array.from(document.querySelectorAll("li.iti__country"));
    var target = items.find(li => {
        var name = li.querySelector(".iti__country-name");
        return name && name.innerText.trim() === "India";
    }) || items.find(li => li.innerText.trim().startsWith("India"));
    
    if (target) {
        target.click();
        return "SELECTED PHONE COUNTRY: " + target.innerText.trim();
    }
    return "NO PHONE COUNTRY TARGET";
})()
"""
res_phone_country = run_js(country_phone_js)
print("PHONE COUNTRY:", res_phone_country)

time.sleep(0.5)

# 3. Fill Text Inputs
fill_text_js = """
(function() {
    function setVal(id, val) {
        var el = document.getElementById(id);
        if (el) {
            el.focus();
            el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
        }
        return false;
    }

    var r = {};
    r.first_name = setVal('first_name', 'Nilesh');
    r.last_name = setVal('last_name', 'Tiwari');
    r.email = setVal('email', 'tiwarivivek2411@gmail.com');
    r.phone = setVal('phone', '8920952855');
    r.linkedin = setVal('question_37811193002', 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    r.pref_name = setVal('question_37811194002', 'Nilesh');
    r.accom = setVal('question_37811198002', 'None required');
    r.gitlab_user = setVal('question_37811199002', 'nileshtiwari');
    r.open_source = setVal('question_37811202002', 'https://github.com/nileshtiwari');
    r.primary_lang = setVal('question_37811203002', 'Java / Spring Boot, Python, Node.js');

    return JSON.stringify(r);
})()
"""
res_text = run_js(fill_text_js)
print("TEXT INPUTS RES:", res_text)

time.sleep(1.0)

# 4. Select Dropdowns
dropdowns = [
    ("question_37811195002", "India"),
    ("question_37811196002", "Yes"),
    ("question_37811197002", "No"),
    ("question_37811200002", "No"),
    ("question_37811201002", "No"),
    ("gender", "Male"),
    ("hispanic_ethnicity", "No"),
    ("veteran_status", "I am not a protected veteran")
]

def select_dropdown(fid, target_text):
    open_js = f"""
    (function() {{
        var inp = document.getElementById("{fid}");
        if (!inp) return "NO_INP";
        inp.scrollIntoView({{ behavior: "smooth", block: "center" }});
        var c = inp.closest(".select__control") || inp.parentElement;
        if (c) {{
            c.dispatchEvent(new MouseEvent("mousedown", {{ bubbles: true }}));
            c.dispatchEvent(new MouseEvent("mouseup", {{ bubbles: true }}));
            c.click();
        }}
        return "OPENED";
    }})()
    """
    run_js(open_js)
    time.sleep(0.5)

    click_js = f"""
    (function() {{
        var lb = document.getElementById("react-select-{fid}-listbox") || document.querySelector("[id*='{fid}-listbox']");
        var opts = lb ? Array.from(lb.querySelectorAll("[id*='-option-']")) : Array.from(document.querySelectorAll("[id*='{fid}-option-']"));
        if (!opts || opts.length === 0) {{
            opts = Array.from(document.querySelectorAll("[id*='-option-']"));
        }}
        var match = opts.find(o => o.innerText.trim().toLowerCase() === "{target_text.lower()}" || o.innerText.trim().toLowerCase().startsWith("{target_text.lower()}"));
        if (match) {{
            match.dispatchEvent(new MouseEvent("mousedown", {{ bubbles: true }}));
            match.dispatchEvent(new MouseEvent("mouseup", {{ bubbles: true }}));
            match.click();
            return "SELECTED: " + match.innerText.trim();
        }}
        return "NOT_FOUND (" + (opts ? opts.map(o => o.innerText.trim()).slice(0, 5).join(", ") : "0") + ")";
    }})()
    """
    res = run_js(click_js)
    print(f"[{fid}] -> {res}")
    time.sleep(0.3)

for fid, opt in dropdowns:
    select_dropdown(fid, opt)

time.sleep(1.5)

# 5. Check Errors
check_errors_js = """
(function() {
    var errs = Array.from(document.querySelectorAll(".error, [class*='error'], [aria-invalid='true']")).map(e => e.innerText.trim()).filter(t => t.length > 0);
    return JSON.stringify(errs);
})()
"""
res_errs = run_js(check_errors_js)
print("FORM ERRORS CHECK:", res_errs)

# 6. Submit Application
submit_js = """
(function() {
    var btn = Array.from(document.querySelectorAll("button")).find(b => b.innerText && b.innerText.trim() === "Submit application");
    if (btn) {
        btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        btn.focus();
        btn.click();
        return "CLICKED SUBMIT";
    }
    return "NO SUBMIT BTN";
})()
"""
res_sub = run_js(submit_js)
print("SUBMIT ACTION:", res_sub)
