import subprocess, json

js_code = """
(function() {
    var emptyFields = [];
    document.querySelectorAll(".field, div[class*='field']").forEach(function(f) {
        var isRequired = f.innerText.includes('*');
        var lbl = f.querySelector('label') ? f.querySelector('label').innerText.trim().replace(/\\n/g, ' ') : '';
        var selectVal = f.querySelector('.select__single-value, [class*=\"singleValue\"]');
        var inp = f.querySelector('input:not([type="hidden"]):not([type="file"]):not([type="submit"]):not([class*="select__input"]), textarea');
        var val = selectVal ? selectVal.innerText.trim() : (inp ? inp.value.trim() : '');
        
        if (isRequired) {
            emptyFields.push({
                label: lbl,
                hasValue: !!val,
                value: val
            });
        }
    });

    var submitBtn = document.querySelector('button[type="submit"], input[type="submit"]');

    return JSON.stringify({
        fields: emptyFields,
        submitBtnFound: !!submitBtn,
        submitBtnDisabled: submitBtn ? submitBtn.disabled : null,
        submitBtnText: submitBtn ? submitBtn.innerText : null
    });
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
print("FINAL VALIDATION CHECK:")
try:
    data = json.loads(out)
    for f in data.get('fields', []):
        status = "✅" if f['hasValue'] else "❌ EMPTY"
        print(f"  {status} {f['label'][:50]}: '{f['value']}'")
    print(f"\nSubmit Button: Found={data.get('submitBtnFound')}, Disabled={data.get('submitBtnDisabled')}, Text='{data.get('submitBtnText')}'")
except Exception as e:
    print(out)
