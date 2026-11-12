import subprocess, time

targets = [
    ("question_64239206", 0), # Use daily
    ("question_65143957", 0), # Yes, both mentoring
    ("question_64239209", 1)  # Less than 15 days
]

for qid, opt_idx in targets:
    # 1. Open
    open_js = f"""
    (function() {{
        var inp = document.getElementById('{qid}');
        if (!inp) return 'NO_INP';
        inp.focus();
        var c = inp.closest('.select__control') || inp.parentElement;
        if (c) {{
            c.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
            c.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
            c.click();
        }}
        return 'OPENED';
    }})()
    """
    cleaned_open = ' '.join([l.strip() for l in open_js.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
    ascript_open = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684133)
            return (execute javascript "{cleaned_open}")
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', ascript_open])
    time.sleep(0.4)

    # 2. Click option inside listbox
    click_js = f"""
    (function() {{
        var lb = document.getElementById('react-select-{qid}-listbox');
        if (!lb) {{
            var allLbs = document.querySelectorAll("[role='listbox'], [id*='listbox']");
            var found = Array.from(allLbs).map(l => l.id);
            return 'LB_NOT_FOUND, found: ' + JSON.stringify(found);
        }}
        var opts = Array.from(lb.querySelectorAll(".select__option, [role='option']"));
        if (opts.length > {opt_idx}) {{
            var opt = opts[{opt_idx}];
            opt.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
            opt.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
            opt.click();
            return 'CLICKED: ' + opt.innerText.trim();
        }}
        return 'OPT_IDX_OUT_OF_BOUNDS';
    }})()
    """
    cleaned_click = ' '.join([l.strip() for l in click_js.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
    ascript_click = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684133)
            return (execute javascript "{cleaned_click}")
        end tell
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, _ = p.communicate(ascript_click)
    print(f"[{qid}] -> {out.strip()}")
    time.sleep(0.3)

print("Finished setting remaining 3 dropdowns!")
