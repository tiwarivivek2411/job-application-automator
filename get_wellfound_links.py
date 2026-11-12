import subprocess, json

js_code = """
(function() {
    var links = Array.from(document.querySelectorAll("a[href*='/jobs/']")).map(function(a) {
        return {
            url: a.href,
            text: a.innerText.trim().replace(/\\n/g, ' ')
        };
    });
    return JSON.stringify(links);
})()
"""

escaped_js = js_code.replace('\n', ' ').replace('"', '\\"')
apple_script = 'tell application "Google Chrome"\n' \
               '    tell (first tab of window 1 whose id is 33684105)\n' \
               f'        return execute javascript "{escaped_js}"\n' \
               '    end tell\n' \
               'end tell'

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(apple_script)
print("OUT:", out[:2000])
if err: print("ERR:", err)
