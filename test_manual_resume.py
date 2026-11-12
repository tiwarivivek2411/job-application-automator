import subprocess, json

js_code = """
(function() {
    var manualBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Enter manually'));
    if (manualBtn) {
        manualBtn.click();
        return 'CLICKED_MANUAL_BTN';
    }
    return 'NO_MANUAL_BTN';
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
print("MANUAL RESUME ACTION:", out)
