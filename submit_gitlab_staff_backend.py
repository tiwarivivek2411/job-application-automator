import subprocess, base64, time, json

TARGET_URL = "gitlab/jobs/8775136002"

def run_js(js):
    b64 = base64.b64encode(js.encode('utf-8')).decode('utf-8')
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "{TARGET_URL}" then
                    return (execute t javascript "eval(atob('{b64}'))")
                end if
            end repeat
        end repeat
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(ascript)
    return out.strip()

print("Checking page...")
print("Title:", run_js("document.title"))

# 1. Attach Resume via DataTransfer
print("\n1. Attaching Resume...")
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
print("\n2. Filling Text Fields...")
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
    r.email = setVal('email', 'tiwarivivek2411@gmail.com');
    r.phone = setVal('phone', '8920952855');
    r.linkedin = setVal('question_38135651002', 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    r.pref_name = setVal('question_38135652002', 'Nilesh');
    r.adjustments = setVal('question_38135656002', 'None');
    r.opensource = setVal('question_38135659002', 'https://github.com/nileshtiwari');
    r.languages = setVal('question_38135660002', 'Java, Spring Boot, Node.js, Python, Kafka, AWS');

    return JSON.stringify(r);
})()
'''
print("Text fields:", run_js(fill_text_js))
time.sleep(0.5)

# 3. Select Dropdowns
print("\n3. Selecting Dropdowns...")
dropdowns = [
    ("country", "India +91"),
    ("question_38135653002", "India"),
    ("question_38135654002", "Yes"),
    ("question_38135655002", "No"),
    ("question_38135657002", "No"),
    ("question_38135658002", "No"),
    ("gender", "Male"),
    ("hispanic_ethnicity", "No"),
    ("veteran_status", "I am not a protected veteran")
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
    time.sleep(0.3)

    click_q_js = f'''
    (() => {{
        var opts = Array.from(document.querySelectorAll('.select__option, [id*="-option-"]'));
        var match = opts.find(o => o.innerText.trim() === "{target_val}" || o.innerText.trim().startsWith("{target_val}"));
        if (match) {{
            match.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
            match.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
            match.click();
            return 'SELECTED: ' + match.innerText.trim();
        }}
        return 'NOT_FOUND: ' + "{target_val}" + ' (opts count: ' + opts.length + ')';
    }})()
    '''
    res = run_js(click_q_js)
    print(f"  [{qid}] -> {res}")
    time.sleep(0.3)

# 4. Check status & Submit button
print("\n4. Checking Submission Status...")
status_js = '''
(() => {
    var submitBtn = Array.from(document.querySelectorAll("button")).find(b => b.innerText && (b.innerText.trim() === "Submit application" || b.innerText.trim() === "Submit Application"));
    var disabled = submitBtn ? submitBtn.disabled || submitBtn.classList.contains('btn__disabled') : null;
    return JSON.stringify({
        btnFound: !!submitBtn,
        disabled: disabled,
        btnClasses: submitBtn ? submitBtn.className : ''
    });
})()
'''
print("Submit Btn:", run_js(status_js))
