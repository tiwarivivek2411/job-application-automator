import subprocess, json

js_code = """
(function() {
    var form = document.querySelector('form');
    var emptyRequired = [];
    document.querySelectorAll('input, select, textarea').forEach(function(i) {
        var isReq = i.required || i.getAttribute('aria-required') === 'true' || (i.closest('.field') && i.closest('.field').innerText.includes('*'));
        if (isReq && !i.value && i.type !== 'hidden' && i.type !== 'file' && i.type !== 'submit') {
            emptyRequired.push({ id: i.id, name: i.name, placeholder: i.placeholder });
        }
    });
    var submitBtn = document.querySelector('button[type="submit"], input[type="submit"]');
    return JSON.stringify({
        emptyRequired: emptyRequired,
        submitBtnText: submitBtn ? submitBtn.innerText : null,
        submitBtnDisabled: submitBtn ? submitBtn.disabled : null
    });
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
print("VALIDATION STATUS:", out)
