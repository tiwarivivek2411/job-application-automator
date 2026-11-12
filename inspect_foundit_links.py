import subprocess, json

js_code = """
(function() {
    var links = [];
    var allA = document.querySelectorAll("a");
    allA.forEach(function(a) {
        if (a.href && (a.href.indexOf("job-desc") !== -1 || a.href.indexOf("/job/") !== -1)) {
            links.push({
                text: a.innerText.trim().replace(/\\n/g, ' '),
                href: a.href
            });
        }
    });
    return JSON.stringify(links.slice(0, 15));
})()
"""

escaped_js = js_code.replace('\n', ' ').replace('"', '\\"')
apple_script = 'tell application "Google Chrome"\n' \
               '    tell (first tab of window 1 whose id is 33684127)\n' \
               f'        return execute javascript "{escaped_js}"\n' \
               '    end tell\n' \
               'end tell'

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(apple_script)
print("LINKS:", out)
if err: print("ERR:", err)
