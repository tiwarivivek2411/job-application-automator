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

# 2. Fill Text Inputs & Textareas
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

    var q1 = "Yes, extensive hands-on experience designing and operating distributed event-driven systems using Apache Kafka, AWS SQS, and Redis streams. At Flipkart and Findem, I engineered event pipelines processing tens of millions of daily messages, implemented idempotent consumers, dead-letter queues, and schema evolution, and orchestrated microservices workflows ensuring high availability and fault tolerance.";
    r.event_driven = setVal('question_19337460004', q1);

    var q2 = "I use AI tools daily (Cursor, Claude Code, GitHub Copilot, and LLM APIs) as an integrated part of my engineering workflow for system design ideation, code generation, test suite synthesis, and reviewing complex PRs. I maintain high rigor by pressure-testing generated code, verifying edge cases, benchmarking latency, and ensuring strict adherence to production-grade architectural standards.";
    r.ai_tools = setVal('question_19337461004', q2);

    var q3 = "At Findem, I automated data enrichment and pipeline validation workflows by building a self-healing asynchronous job runner with automatic retry backoffs, distributed caching, and automated dead-letter queue alerting. This reduced manual pipeline interventions by 85% and cut pipeline execution latency by 40%.";
    r.automated = setVal('question_19337462004', q3);

    r.comp = setVal('question_19337464004', '42 LPA (INR 42,00,000)');
    r.notice = setVal('question_19337465004', '15 Days / Immediate. Available to join immediately.');
    r.linkedin = setVal('question_19337468004', 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');

    return JSON.stringify(r);
})()
"""
res_text = run_js(fill_text_js)
print("TEXT INPUTS RES:", res_text)

time.sleep(1.0)

# 3. Select Dropdowns
dropdowns = [
    ("country", "India"),
    ("question_19941764004", "Yes"),
    ("question_19337466004", "No"),
    ("question_19337467004", "Yes"),
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
        var opts = Array.from(document.querySelectorAll("[id*='-option-']"));
        var match = opts.find(o => o.innerText.trim() === "{opt_target}" || o.innerText.trim().startsWith("{opt_target}"));
        if (match) {{
            match.dispatchEvent(new MouseEvent("mousedown", {{ bubbles: true }}));
            match.dispatchEvent(new MouseEvent("mouseup", {{ bubbles: true }}));
            match.click();
            return "SELECTED: " + match.innerText.trim();
        }}
        return "NOT_FOUND: " + "{opt_target}" + " (opts=" + opts.length + ")";
    }})()
    """
    res_click = run_js(click_js)
    print(f"[{fid}] -> {res_click}")
    time.sleep(0.3)

time.sleep(1.5)

# 4. Check for errors
check_errors_js = """
(function() {
    var errs = Array.from(document.querySelectorAll(".error, [class*='error'], [aria-invalid='true']")).map(e => e.innerText.trim()).filter(t => t.length > 0);
    var btn = Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "Submit application");
    return JSON.stringify({
        errors: errs,
        btnDisabled: btn ? btn.disabled : true
    });
})()
"""
res_errs = run_js(check_errors_js)
print("FORM ERRORS CHECK:", res_errs)

# 5. Submit
submit_js = """
(function() {
    var btn = Array.from(document.querySelectorAll("button")).find(b => b.innerText.trim() === "Submit application");
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
