import subprocess, json

js_code = """
(function() {
    var ta = document.querySelector('textarea#resume_text, textarea');
    return JSON.stringify({
        hasTextarea: !!ta,
        id: ta ? ta.id : null,
        name: ta ? ta.name : null,
        placeholder: ta ? ta.placeholder : null,
        visible: ta ? (ta.offsetWidth > 0 && ta.offsetHeight > 0) : false
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
print("TEXTAREA:", out)
