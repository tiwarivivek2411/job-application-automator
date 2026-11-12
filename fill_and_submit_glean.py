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

# 1. Fill Text Inputs
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
    r.linkedin = setVal('question_4021092005', 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    r.website = setVal('question_4021093005', 'https://github.com/nileshtiwari');
    r.exp = setVal('question_8504960005', '4.5');
    
    var aiText = "I actively use LLMs and AI coding agents daily (Cursor, Claude Code, GitHub Copilot, and LLM APIs) to accelerate architecture design, test writing, and complex system refactoring, as well as integrating vector embeddings and RAG pipelines for contextual retrieval.";
    r.ai_tools = setVal('question_8595582005', aiText);

    return JSON.stringify(r);
})()
"""
res_text = run_js(fill_text_js)
print("TEXT INPUTS RES:", res_text)

time.sleep(1.0)

# 2. Select React-Select Dropdowns
dropdowns = [
    ("question_7132748005", "LinkedIn"),
    ("gender", "Male"),
    ("hispanic_ethnicity", "No"),
    ("veteran_status", "I am not a protected veteran")
]

for fid, opt_target in dropdowns:
    open_js = f"""
    (function() {{
        var inp = document.getElementById("{fid}");
        if (!inp) return "NO_INP";
        var control = inp.closest(".select__control") || inp.parentElement;
        if (control) {{
            control.dispatchEvent(new MouseEvent("mousedown", {{ bubbles: true }}));
            control.dispatchEvent(new MouseEvent("mouseup", {{ bubbles: true }}));
            control.click();
        }}
        return "OPENED";
    }})()
    """
    run_js(open_js)
    time.sleep(0.4)

    click_js = f"""
    (function() {{
        var opts = Array.from(document.querySelectorAll(".select__option, [id*='-option-']"));
        var match = opts.find(o => o.innerText.trim() === "{opt_target}" || o.innerText.trim().startsWith("{opt_target}"));
        if (match) {{
            match.dispatchEvent(new MouseEvent("mousedown", {{ bubbles: true }}));
            match.dispatchEvent(new MouseEvent("mouseup", {{ bubbles: true }}));
            match.click();
            return "SELECTED: " + match.innerText.trim();
        }}
        return "NOT_FOUND: " + "{opt_target}";
    }})()
    """
    res_click = run_js(click_js)
    print(f"[{fid}] -> {res_click}")
    time.sleep(0.3)

time.sleep(1.5)

# 3. Check for errors
check_errors_js = """
(function() {
    var errs = Array.from(document.querySelectorAll(".error, [class*='error'], [aria-invalid='true']")).map(e => e.innerText.trim()).filter(t => t.length > 0);
    var btn = document.querySelector("button[type='submit']");
    return JSON.stringify({
        errors: errs,
        btnText: btn ? btn.innerText.trim() : "NO BTN",
        btnDisabled: btn ? btn.disabled : true
    });
})()
"""
res_errs = run_js(check_errors_js)
print("FORM CHECK:", res_errs)

# 4. Submit
submit_js = """
(function() {
    var btn = document.querySelector("button[type='submit']");
    if (btn && !btn.disabled) {
        btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        btn.focus();
        btn.click();
        return "CLICKED_SUBMIT";
    }
    return "CANNOT_SUBMIT";
})()
"""
res_sub = run_js(submit_js)
print("SUBMIT ACTION:", res_sub)
