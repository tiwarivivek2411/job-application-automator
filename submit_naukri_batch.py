import subprocess, time

js_code = """
(function() {
    var checkIds = [
        "jobTupleCheck-1",
        "jobTupleCheck-18",
        "jobTupleCheck-26",
        "jobTupleCheck-36",
        "jobTupleCheck-45"
    ];
    var selected = [];
    checkIds.forEach(function(id) {
        var el = document.getElementById(id);
        if (el) {
            var label = el.closest("label") || document.querySelector("label[for='" + id + "']");
            if (label && !el.checked) {
                label.click();
                selected.push(id + " (via label)");
            } else if (!el.checked) {
                el.click();
                selected.push(id + " (direct)");
            } else {
                selected.push(id + " (already checked)");
            }
        } else {
            selected.push(id + " (NOT FOUND)");
        }
    });
    
    // Now find multi-apply button
    var multiBtn = document.querySelector(".multi-apply-button, [class*='multiApply'], button[id*='apply']");
    var btnClicked = false;
    if (multiBtn) {
        multiBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        multiBtn.click();
        btnClicked = true;
    }
    return JSON.stringify({ selected: selected, btnClicked: btnClicked, btnText: multiBtn ? multiBtn.innerText : null });
})()
"""

escaped_js = js_code.replace('\n', ' ').replace('"', '\\"')
apple_script = 'tell application "Google Chrome"\n' \
               '    tell (first tab of window 1 whose id is 33684098)\n' \
               f'        return execute javascript "{escaped_js}"\n' \
               '    end tell\n' \
               'end tell'

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(apple_script)
print("MULTI APPLY RESULT:", out)
if err: print("ERR:", err)
