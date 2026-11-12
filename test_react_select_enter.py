import subprocess, json, time

js_test = """
(function() {
    // Click body to close any open dropdowns
    document.body.click();

    var inp = document.getElementById('question_64239203');
    if (!inp) return 'NO_INP';
    inp.focus();
    inp.value = '3 - 5';
    inp.dispatchEvent(new Event('input', { bubbles: true }));
    inp.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true }));
    inp.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', keyCode: 13, bubbles: true }));

    // Check singleValue or value container
    var container = inp.closest('.select__control');
    var valText = container ? container.innerText : '';
    return 'CONTAINER_TEXT: ' + valText.replace(/\\n/g, ' ');
})()
"""

cleaned = ' '.join([l.strip() for l in js_test.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{cleaned}")
    end tell
end tell
'''
p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("TYPE + ENTER RESULT:", out)
