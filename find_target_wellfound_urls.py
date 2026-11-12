import subprocess, json

js_code = """
(function() {
    var targets = ['parsewave', 'fledgehealth', 'richpanel', 'discovered', 'azodha'];
    var found = [];
    var links = document.querySelectorAll('a');
    links.forEach(function(a) {
        var href = a.href || '';
        var txt = a.innerText.toLowerCase();
        for (var i = 0; i < targets.length; i++) {
            var t = targets[i];
            if (href.toLowerCase().includes(t) || txt.includes(t)) {
                found.push({ target: t, href: href, text: a.innerText.trim().replace(/\\n/g, ' ') });
                break;
            }
        }
    });
    return JSON.stringify(found);
})()
"""

cleaned_lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
escaped = ' '.join(cleaned_lines).replace('\\', '\\\\').replace('"', '\\"')

ascript = f'''
tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (URL of t as string) contains "wellfound.com" then
                return (execute t javascript "{escaped}")
            end if
        end repeat
    end repeat
    return "NO_TAB"
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("MATCHED URLS:", out)
if err: print("ERR:", err)
