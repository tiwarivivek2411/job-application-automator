import subprocess, json

js_code = """
(function() {
    var selects = [];
    document.querySelectorAll(".select__input, [role='combobox']").forEach(function(inp) {
        var id = inp.id;
        var labelEl = document.querySelector("label[for='" + id + "']") || document.getElementById(id + "-label");
        selects.push({
            id: id,
            label: labelEl ? labelEl.innerText.trim() : ""
        });
    });
    return JSON.stringify(selects);
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
print("REACT SELECTS:", out)
