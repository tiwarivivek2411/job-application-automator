import subprocess, base64, time, json

TAB_ID = 33684280

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

# 1. Attach Resume via DataTransfer
print("1. Attaching Resume...")
with open('/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf', 'rb') as f:
    pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

attach_js = f'''
(() => {{
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
        if (!fileInput) return "NO_RESUME_INPUT";

        var dt = new DataTransfer();
        dt.items.add(file);
        fileInput.files = dt.files;
        fileInput.dispatchEvent(new Event("change", {{ bubbles: true }}));
        fileInput.dispatchEvent(new Event("input", {{ bubbles: true }}));

        return "ATTACH_SUCCESS: " + fileInput.files[0].name;
    }} catch (e) {{
        return "ERROR: " + e.message;
    }}
}})()
'''
print("Attach:", run_js(attach_js))
time.sleep(1.0)

# 2. Fill text fields
print("2. Filling Text Fields...")
fill_text_js = '''
(() => {
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
    r.preferred_name = setVal('preferred_name', 'Nilesh');
    r.email = setVal('email', 'tiwarivivek2411@gmail.com');
    r.phone = setVal('phone', '8920952855');
    r.pref_last = setVal('question_31426469003', 'Tiwari');
    r.zip = setVal('question_31426470003', '560103');
    r.linkedin = setVal('question_31426471003', 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    r.company = setVal('question_31426472003', 'Alrium Technologies');

    return JSON.stringify(r);
})()
'''
print("Text fields:", run_js(fill_text_js))
time.sleep(1.0)

# 3. Select Country (India)
print("3. Selecting Country (India)...")
country_js = '''
(() => {
    var inp = document.getElementById('country');
    if (!inp) return 'NO_COUNTRY';
    inp.scrollIntoView({block: 'center'});
    var ctrl = inp.closest('.select__control');
    ctrl.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
    ctrl.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
    ctrl.click();
    return 'OPENED_COUNTRY';
})()
'''
run_js(country_js)
time.sleep(0.5)

country_opt_js = '''
(() => {
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
'''
print("Country opt:", run_js(country_opt_js))
time.sleep(0.5)

# 4. Select Candidate Location (Bengaluru)
print("4. Selecting Candidate Location (Bengaluru)...")
loc_open_js = '''
(() => {
    var inp = document.getElementById('candidate-location');
    if (!inp) return 'NO_LOC';
    inp.scrollIntoView({block: 'center'});
    inp.focus();
    var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    nativeInputValueSetter.call(inp, 'Bengaluru');
    inp.dispatchEvent(new Event('input', { bubbles: true }));
    inp.dispatchEvent(new KeyboardEvent('keydown', { key: 'a', bubbles: true }));
    inp.dispatchEvent(new KeyboardEvent('keyup', { key: 'a', bubbles: true }));
    return 'DISPATCHED_LOC';
})()
'''
run_js(loc_open_js)
time.sleep(1.5)

loc_opt_js = '''
(() => {
    var opt = document.getElementById('react-select-candidate-location-option-0');
    if (opt) {
        opt.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
        opt.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
        opt.click();
        return 'CLICKED OPT 0: ' + opt.innerText.trim();
    }
    var opts = Array.from(document.querySelectorAll("[id*='-option-']"));
    var target = opts.find(o => o.innerText.trim().toLowerCase().includes('bengaluru') || o.innerText.trim().toLowerCase().includes('bangalore'));
    if (target) {
        target.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
        target.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
        target.click();
        return 'SELECTED LOC: ' + target.innerText.trim();
    }
    return 'LOC NOT FOUND: ' + opts.map(o => o.innerText.trim()).join(', ');
})()
'''
print("Location opt:", run_js(loc_opt_js))
time.sleep(1.0)

# 5. Select Dropdown Questions
print("5. Selecting Dropdown Questions...")
dropdowns = [
    ("question_31426473003", "Yes"), # eligible to work in India
    ("question_31426474003", "No"),  # need sponsorship
    ("question_31426475003", "No"),  # currently employee/contractor at Abnormal
    ("question_31426476003", "No"),  # previously worked at Abnormal
    ("question_31585753003", "Yes")  # comfortable with hybrid model in Bangalore
]

for qid, target_val in dropdowns:
    open_q_js = f'''
    (() => {{
        var inp = document.getElementById('{qid}');
        if (!inp) return 'NO_INP';
        inp.scrollIntoView({{block: 'center'}});
        var ctrl = inp.closest('.select__control') || inp.parentElement;
        if (ctrl) {{
            ctrl.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
            ctrl.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
            ctrl.click();
        }}
        inp.focus();
        return 'OPENED';
    }})()
    '''
    run_js(open_q_js)
    time.sleep(0.4)

    click_q_js = f'''
    (() => {{
        var opts = Array.from(document.querySelectorAll('.select__option, [id*="-option-"]'));
        var match = opts.find(o => o.innerText.trim().toLowerCase().includes("{target_val.lower()}"));
        if (match) {{
            match.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
            match.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
            match.click();
            return 'SELECTED: ' + match.innerText.trim();
        }}
        return 'NOT_FOUND: ' + "{target_val}" + ' (opts: ' + opts.map(o => o.innerText.trim()).join(', ') + ')';
    }})()
    '''
    res = run_js(click_q_js)
    print(f"  [{qid}] -> {res}")
    time.sleep(0.4)

# 6. Verify form and submit
print("\n6. Checking Form Readiness...")
check_errs_js = '''
(() => {
    var errs = Array.from(document.querySelectorAll('.error, [class*="error"], [aria-invalid="true"]')).map(e => e.innerText ? e.innerText.trim() : e.id).filter(Boolean);
    var submitBtn = Array.from(document.querySelectorAll("button")).find(b => b.innerText && b.innerText.trim() === "Submit application");
    return JSON.stringify({
        errors: errs,
        submitFound: !!submitBtn,
        submitDisabled: submitBtn ? submitBtn.disabled : null
    });
})()
'''
print("Status:", run_js(check_errs_js))

# Submit
print("7. Submitting Application...")
submit_js = '''
(() => {
    var btn = Array.from(document.querySelectorAll("button")).find(b => b.innerText && b.innerText.trim() === "Submit application");
    if (btn) {
        btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        btn.focus();
        btn.click();
        return "CLICKED_SUBMIT";
    }
    return "NO_SUBMIT_BTN";
})()
'''
print("Submit result:", run_js(submit_js))

time.sleep(6.0)

check_post_js = '''
(() => {
    return JSON.stringify({
        url: window.location.href,
        snippet: document.body.innerText.substring(0, 500)
    });
})()
'''
print("Post-submission:", run_js(check_post_js))
