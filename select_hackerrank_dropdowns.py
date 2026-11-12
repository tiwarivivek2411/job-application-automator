import subprocess, json, time

dropdown_selections = [
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

for fid, opt_target in dropdown_selections:
    # 1. Open dropdown
    open_js = f"""
    (function() {{
        var inp = document.getElementById('{fid}');
        if (!inp) return 'NO_INP';
        var control = inp.closest('.select__control') || inp.parentElement;
        if (control) {{
            control.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
            control.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
            control.click();
        }}
        inp.focus();
        return 'OPENED';
    }})()
    """
    res_open = run_js(open_js)
    time.sleep(0.35)

    # 2. Click option
    click_js = f"""
    (function() {{
        var opts = Array.from(document.querySelectorAll('.select__option, [id*="-option-"]'));
        var match = opts.find(o => o.innerText.trim() === "{opt_target}" || o.innerText.trim().startsWith("{opt_target}"));
        if (match) {{
            match.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
            match.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
            match.click();
            return 'SELECTED: ' + match.innerText.trim();
        }}
        return 'NOT_FOUND: ' + "{opt_target}" + ' (found ' + opts.length + ' opts)';
    }})()
    """
    res_click = run_js(click_js)
    print(f"[{fid}] -> {res_click}")
    time.sleep(0.3)

print("All dropdowns processed!")
