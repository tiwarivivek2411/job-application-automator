import subprocess, json

js_code = """
(function() {
    var fields = [];
    document.querySelectorAll(".field").forEach(function(f) {
        var lbl = f.querySelector("label") ? f.querySelector("label").innerText.trim().replace(/\\n/g, ' ') : '';
        var val = '';
        var inp = f.querySelector("input, select, textarea");
        var selectVal = f.querySelector(".select__single-value, [class*='singleValue']");
        if (selectVal) {
            val = selectVal.innerText.trim();
        } else if (inp) {
            val = inp.value;
        }
        if (lbl) {
            fields.push({ label: lbl, value: val });
        }
    });
    return JSON.stringify(fields);
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
print("FIELDS & VALUES:")
try:
    items = json.loads(out)
    for i in items:
        print(f"  {i['label'][:60]} -> '{i['value']}'")
except Exception as e:
    print(out)
