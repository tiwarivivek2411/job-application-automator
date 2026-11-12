import subprocess, json

js_code = """
(function() {
    var allA = document.querySelectorAll("a[href*='/jobs/']");
    var map = {};
    allA.forEach(function(a) {
        var href = a.href;
        if (href.indexOf('/jobs/') !== -1 && !href.endsWith('/jobs')) {
            var txt = a.innerText.trim().replace(/\\n/g, ' ');
            if (!map[href] || txt.length > map[href].length) {
                map[href] = txt;
            }
        }
    });
    var res = [];
    for (var k in map) {
        res.push({ href: k, text: map[k] });
    }
    return JSON.stringify(res);
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
try:
    items = json.loads(out)
    print(f"Total Wellfound Job URLs found: {len(items)}")
    for i in items:
        print(f"  {i['href']} -> {i['text'][:60]}")
except Exception as e:
    print("RAW:", out)
    if err: print("ERR:", err)
