import subprocess, time

js_code = """
(function() {
    // Uncheck everything first
    document.querySelectorAll("input[type='checkbox']:checked").forEach(cb => {
        var lbl = cb.closest("label") || document.querySelector("label[for='" + cb.id + "']");
        if (lbl) lbl.click(); else cb.click();
    });

    var targetCheckIds = [
        "jobTupleCheck-26",
        "jobTupleCheck-36",
        "jobTupleCheck-45",
        "jobTupleCheck-50",
        "jobTupleCheck-65"
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

    var multiBtn = document.querySelector(".multi-apply-button");
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

cleaned_lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
escaped = ' '.join(cleaned_lines).replace('\\', '\\\\').replace('"', '\\"')

ascript = f'''
tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (URL of t as string) contains "naukri.com/mnjuser" then
                return (execute t javascript "{escaped}")
            end if
        end repeat
    end repeat
    return "NO_TAB"
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("NAUKRI BATCH 2 SUBMIT:", out)
if err: print("ERR:", err)
