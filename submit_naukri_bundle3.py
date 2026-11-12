import subprocess, base64, time, json

def run_js(js):
    b64 = base64.b64encode(js.encode('utf-8')).decode('utf-8')
    ascript = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684098)
            return (execute javascript "eval(atob('{b64}'))")
        end tell
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(ascript)
    return out.strip()

check_and_apply_js = """
(() => {
    // Uncheck everything first
    document.querySelectorAll("input[type='checkbox']:checked").forEach(cb => {
        var lbl = cb.closest("label") || document.querySelector("label[for='" + cb.id + "']");
        if (lbl) lbl.click(); else cb.click();
    });

    var targetCheckIds = [
        "jobTupleCheck-1",
        "jobTupleCheck-19",
        "jobTupleCheck-25",
        "jobTupleCheck-26",
        "jobTupleCheck-32"
    ];

    var checked = [];
    targetCheckIds.forEach(function(id) {
        var el = document.getElementById(id);
        if (el) {
            var label = el.closest("label") || document.querySelector("label[for='" + id + "']");
            if (label && !el.checked) {
                label.click();
                checked.push(id);
            } else if (!el.checked) {
                el.click();
                checked.push(id);
            }
        }
    });

    var multiBtn = document.querySelector(".multi-apply-button, button.multi-apply");
    var clicked = false;
    if (multiBtn && !multiBtn.disabled) {
        multiBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        multiBtn.click();
        clicked = true;
    }

    return JSON.stringify({
        checked: checked,
        clicked: clicked,
        btnDisabled: multiBtn ? multiBtn.disabled : null
    });
})()
"""

res = run_js(check_and_apply_js)
print("MULTI-APPLY RES:", res)

time.sleep(2.0)

# Check drawer or toast
check_drawer_js = """
(() => {
    var drawer = document.querySelector('.drawer-wrapper, .chatbot_drawer, [class*="drawer"]');
    var toast = document.querySelector('.toast, [class*="toast"], .naukri-toast');
    return JSON.stringify({
        drawerVisible: drawer ? drawer.offsetWidth > 0 : false,
        drawerText: drawer ? drawer.innerText.slice(0, 200) : '',
        toastText: toast ? toast.innerText.slice(0, 200) : ''
    });
})()
"""
print("DRAWER/TOAST:", run_js(check_drawer_js))
