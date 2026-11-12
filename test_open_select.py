import subprocess, json, time

js_code = """
(function() {
    var inp = document.getElementById('question_64239203');
    if (!inp) return 'NO_INP';
    var control = inp.closest('.select__control') || inp.parentElement;
    if (control) {
        control.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        control.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
        control.click();
    }
    inp.focus();
    return 'CLICKED_CONTROL';
})()
"""

cleaned_lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
escaped = ' '.join(cleaned_lines).replace('\\', '\\\\').replace('"', '\\"')

ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{escaped}")
    end tell
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("OPEN MENU:", out)

time.sleep(1)

js_opts = """
(function() {
    var opts = Array.from(document.querySelectorAll('.select__option, [id*="-option-"]')).map(o => o.innerText.trim());
    return JSON.stringify(opts);
})()
"""
escaped_opts = ' '.join([l.strip() for l in js_opts.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
ascript2 = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{escaped_opts}")
    end tell
end tell
'''
p2 = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out2, err2 = p2.communicate(ascript2)
print("RENDERED OPTIONS:", out2)
