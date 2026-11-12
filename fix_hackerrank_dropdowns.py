import subprocess, json, time

dropdown_map = [
    ("country", "India +91"),
    ("question_64239203", "3 - 5 Years"),
    ("question_64239204", "Java / Spring Boot"),
    ("question_64239205", "Yes"),
    ("question_65143956", "Yes, multiple times"),
    ("question_64239206", "Use daily"),
    ("question_65143957", "Yes, both mentoring and leading cross-team projects"),
    ("question_64239208", "Yes"),
    ("question_64239209", "Less than 15 days"),
    ("question_64239211", "No")
]

def run_js(js):
    cleaned = ' '.join([l.strip() for l in js.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
    ascript = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684133)
            return (execute javascript "{cleaned}")
        end tell
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(ascript)
    return out.strip()

for qid, target_val in dropdown_map:
    select_js = f"""
    (function() {{
        var inp = document.getElementById('{qid}');
        if (!inp) return 'NO_INP: ' + '{qid}';
        
        // Focus and click the control
        var control = inp.closest('.select__control') || inp.parentElement;
        if (control) {{
            control.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
            control.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
            control.click();
        }}
        inp.focus();

        // Search specifically within options that match this question id
        var opts = Array.from(document.querySelectorAll("[id*='{qid}-option-'], .select__option"));
        var match = opts.find(o => o.innerText.trim() === "{target_val}" || o.innerText.trim().startsWith("{target_val}"));
        if (match) {{
            match.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
            match.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
            match.click();
            return 'SUCCESS: ' + match.innerText.trim();
        }}
        return 'NOT_FOUND: ' + "{target_val}" + ' in ' + opts.length + ' opts';
    }})()
    """
    res = run_js(select_js)
    print(f"[{qid}] -> {res}")
    time.sleep(0.4)

print("Finished setting all dropdowns!")
