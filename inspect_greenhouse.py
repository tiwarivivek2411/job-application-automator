import subprocess, json

js_code = """
(function() {
    var title = document.title;
    var h1 = document.querySelector('h1') ? document.querySelector('h1').innerText : '';
    var form = document.querySelector('form');
    var inputs = [];
    document.querySelectorAll('input, select, textarea, button').forEach(function(i) {
        var lbl = '';
        if (i.id) {
            var l = document.querySelector("label[for='" + i.id + "']");
            if (l) lbl = l.innerText.trim();
        }
        if (!lbl && i.closest('label')) {
            lbl = i.closest('label').innerText.trim();
        }
        if (!lbl && i.placeholder) {
            lbl = i.placeholder;
        }
        inputs.push({
            tag: i.tagName,
            type: i.type,
            name: i.name,
            id: i.id,
            label: lbl.replace(/\\n/g, ' '),
            text: i.innerText ? i.innerText.trim() : ''
        });
    });
    return JSON.stringify({
        title: title,
        h1: h1,
        hasForm: !!form,
        inputs: inputs
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
try:
    data = json.loads(out)
    print("Page Title:", data.get('title'))
    print("H1:", data.get('h1'))
    print(f"Total Inputs: {len(data.get('inputs', []))}")
    for inp in data.get('inputs', []):
        if inp['tag'] in ['INPUT', 'SELECT', 'TEXTAREA', 'BUTTON'] and (inp['label'] or inp['name'] or inp['text']):
            print(f"  [{inp['tag']}] name='{inp['name']}' id='{inp['id']}' type='{inp['type']}' label='{inp['label'][:50]}' text='{inp['text'][:30]}'")
except Exception as e:
    print("RAW:", out[:1500])
    if err: print("ERR:", err)
