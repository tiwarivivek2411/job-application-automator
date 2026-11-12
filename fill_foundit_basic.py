import subprocess, time

js_code = """
(function() {
    function setVal(selector, val) {
        var el = document.querySelector(selector);
        if (el) {
            el.focus();
            el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
        }
        return false;
    }

    var res = {};
    res['fullName'] = setVal('#fullName', 'Nilesh Tiwari');
    
    // Male radio (option-0)
    var maleRadio = document.getElementById('option-0');
    if (maleRadio) {
        var label = maleRadio.closest('label') || document.querySelector("label[for='option-0']");
        if (label) label.click(); else maleRadio.click();
        res['gender'] = 'MALE_CLICKED';
    }

    // Experience: 4 Years, 6 Months
    res['exp_years'] = setVal('#totalExperience', '4');
    res['exp_months'] = setVal('#totalExperienceMonth', '6');

    // Location: Bengaluru
    res['location'] = setVal('#currentLocation', 'Bengaluru');

    return JSON.stringify(res);
})()
"""

cleaned = ' '.join([l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')

ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684127)
        return (execute javascript "{cleaned}")
    end tell
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("FILL BASIC DETAILS OUT:\n", out.strip())
