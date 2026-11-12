import subprocess, json, time

fields = [
    ("country", "India"),
    ("question_64239203", "experience"),
    ("question_64239204", "primary stack"),
    ("question_64239205", "sql/nosql schema"),
    ("question_65143956", "architecture"),
    ("question_64239206", "ai tools"),
    ("question_65143957", "mentored"),
    ("question_64239208", "relocate bangalore"),
    ("question_64239209", "notice period"),
    ("question_64239211", "offers")
]

results = {}

for fid, desc in fields:
    js_open = f"""
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
    cleaned = ' '.join([l.strip() for l in js_open.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
    ascript = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684133)
            return (execute javascript "{cleaned}")
        end tell
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, _ = p.communicate(ascript)
    time.sleep(0.4)

    js_get = """
    (function() {
        var opts = Array.from(document.querySelectorAll('.select__option, [id*="-option-"]')).map(o => o.innerText.trim());
        return JSON.stringify(opts);
    })()
    """
    cleaned_get = ' '.join([l.strip() for l in js_get.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
    ascript_get = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684133)
            return (execute javascript "{cleaned_get}")
        end tell
    end tell
    '''
    p2 = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out2, _ = p2.communicate(ascript_get)
    try:
        opts = json.loads(out2)
    except Exception:
        opts = [out2]
    results[fid] = { "desc": desc, "options": opts }

print(json.dumps(results, indent=2))
