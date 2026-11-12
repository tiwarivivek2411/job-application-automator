import subprocess, json, base64, time

TAB_ID = 33684133

def run_js(js):
    b64 = base64.b64encode(js.encode('utf-8')).decode('utf-8')
    ascript = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is {TAB_ID})
            return (execute javascript "eval(atob('{b64}'))")
        end tell
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(ascript)
    return out.strip()

print("1. Attaching Resume...")
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

print("2. Filling Text Fields...")
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
    r.pref_name = setVal('preferred_name', 'Nilesh');
    r.email = setVal('email', 'tiwarivivek2411@gmail.com');
    r.phone = setVal('phone', '8920952855');
    r.linkedin = setVal('question_18675698008', 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');

    return JSON.stringify(r);
})()
"""
res_text = run_js(fill_text_js)
print("TEXT RES:", res_text)

time.sleep(0.5)

print("3. Selecting Country (India +91)...")
country_js = """
(function() {
    var inp = document.getElementById('country');
    if (!inp) return 'NO_COUNTRY';
    inp.scrollIntoView({block: 'center'});
    var ctrl = inp.closest('.select__control');
    ctrl.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
    ctrl.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
    ctrl.click();
    return 'OPENED_COUNTRY';
})()
"""
run_js(country_js)
time.sleep(0.5)

country_opt_js = """
(function() {
    var opts = Array.from(document.querySelectorAll("[id*='-option-']"));
    var ind = opts.find(o => o.innerText.trim().startsWith('India'));
    if (ind) {
        ind.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
        ind.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
        ind.click();
        return 'SELECTED: ' + ind.innerText.trim();
    }
    return 'NOT_FOUND';
})()
"""
res_country = run_js(country_opt_js)
print("COUNTRY OPT RES:", res_country)

time.sleep(0.5)

print("4. Selecting Candidate Location (Bengaluru)...")
loc_open_js = """
(function() {
    var inp = document.getElementById('candidate-location');
    if (!inp) return 'NO_LOC';
    inp.scrollIntoView({block: 'center'});
    var ctrl = inp.closest('.select__control');
    ctrl.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
    ctrl.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
    ctrl.click();
    return 'OPENED_LOC';
})()
"""
run_js(loc_open_js)
time.sleep(0.6)

loc_opt_js = """
(function() {
    var opts = Array.from(document.querySelectorAll("[id*='-option-']"));
    var target = opts.find(o => o.innerText.trim().toLowerCase().includes('bengaluru') || o.innerText.trim().toLowerCase().includes('bangalore'));
    if (target) {
        target.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
        target.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
        target.click();
        return 'SELECTED LOC: ' + target.innerText.trim();
    }
    return 'LOC NOT FOUND';
})()
"""
res_loc = run_js(loc_opt_js)
print("LOC RES:", res_loc)

time.sleep(0.5)

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
        var opts = Array.from(document.querySelectorAll("[id*='-option-']"));
        var match = opts.find(o => o.innerText.trim().toLowerCase() === "{target_text.lower()}");
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

print("5. Selecting Eligibility (Yes) & Sponsorship (No)...")
select_dropdown("question_18675696008", "Yes")
select_dropdown("question_18675697008", "No")

time.sleep(1.0)

print("6. Checking Errors...")
check_errs_js = """
(function() {
    var errs = Array.from(document.querySelectorAll('.error, [class*="error"], [aria-invalid="true"]')).map(e => e.innerText ? e.innerText.trim() : e.id).filter(Boolean);
    return JSON.stringify(errs);
})()
"""
print("ERRORS:", run_js(check_errs_js))

print("7. Submitting Application...")
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

time.sleep(3.5)
check_url_js = """
(() => {
    return window.location.href + ' ||| ' + document.body.innerText.slice(0, 300);
})()
"""
print("FINAL PAGE:", run_js(check_url_js))
