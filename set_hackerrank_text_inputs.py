import subprocess, json

js_code = """
(function() {
    function setVal(selector, val) {
        var el = document.querySelector(selector);
        if (el) {
            el.focus();
            el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            return el.value;
        }
        return 'NOT_FOUND';
    }

    var textInputs = {};
    textInputs['first_name'] = setVal('#first_name', 'Nilesh');
    textInputs['last_name'] = setVal('#last_name', 'Tiwari');
    textInputs['email'] = setVal('#email', 'tiwarivivek2411@gmail.com');
    textInputs['phone'] = setVal('#phone', '8920952855');

    // Find location, salary, linkedin, github inputs by their label
    document.querySelectorAll('.field, div[class*="field"]').forEach(function(f) {
        var lbl = f.querySelector('label') ? f.querySelector('label').innerText.trim() : '';
        var inp = f.querySelector('input[type="text"], input:not([type]), textarea');
        if (inp && !inp.className.includes('select__input')) {
            if (lbl.includes('current location')) {
                setVal('#' + inp.id, 'Bengaluru, Karnataka');
                textInputs['location'] = inp.value;
            } else if (lbl.includes('salary')) {
                setVal('#' + inp.id, '42 LPA');
                textInputs['salary'] = inp.value;
            } else if (lbl.includes('LinkedIn')) {
                setVal('#' + inp.id, 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
                textInputs['linkedin'] = inp.value;
            } else if (lbl.includes('Github') || lbl.includes('Website')) {
                setVal('#' + inp.id, 'https://github.com/nileshtiwari');
                textInputs['github'] = inp.value;
            }
        }
    });

    return JSON.stringify(textInputs);
})()
"""

cleaned = ' '.join([l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')

ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{cleaned}")
    end tell
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("TEXT INPUTS SET:", out)
if err: print("ERR:", err)
