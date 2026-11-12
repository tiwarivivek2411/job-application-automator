import subprocess, json, time

time.sleep(3)
js_code = """
(function() {
    var title = document.title;
    var form = document.querySelector('form');
    var inputs = [];
    document.querySelectorAll('input, select, textarea, button').forEach(function(i) {
        var lbl = '';
        var p = i.closest('.field') || i.closest('[class*="field"]') || i.parentElement;
        var l = p ? p.querySelector('label') : null;
        if (l) lbl = l.innerText.trim();
        if (!lbl && i.placeholder) lbl = i.placeholder;
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
        inputs: inputs,
        bodySnippet: document.body.innerText.slice(0, 1000).replace(/\\n/g, ' ')
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
try:
    data = json.loads(out)
    print("PAGE TITLE:", data.get('title'))
    print("BODY SNIPPET:", data.get('bodySnippet')[:400])
    print(f"Total Inputs: {len(data.get('inputs', []))}")
    for inp in data.get('inputs', []):
        if inp['tag'] in ['INPUT', 'SELECT', 'TEXTAREA', 'BUTTON'] and (inp['label'] or inp['name'] or inp['text']):
            print(f"  [{inp['tag']}] name='{inp['name']}' id='{inp['id']}' type='{inp['type']}' label='{inp['label'][:50]}' text='{inp['text'][:30]}'")
except Exception as e:
    print(out)
    if err: print("ERR:", err)
