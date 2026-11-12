import subprocess, json

js_code = """
(function() {
    var cards = document.querySelectorAll(".srpResultCard, div[class*='cardContainer'], div[class*='srpResultCard']");
    var details = [];
    cards.forEach(function(c, i) {
        if (i < 5) {
            var t = c.querySelector(".jobTitle, [class*='jobTitle'], h3, a[href*='job-desc']");
            var comp = c.querySelector(".companyName, [class*='companyName']");
            var links = Array.from(c.querySelectorAll("a")).map(a => a.href);
            var buttons = Array.from(c.querySelectorAll("button, div[role='button']")).map(b => b.innerText.trim());
            details.push({
                index: i,
                title: t ? t.innerText.trim() : "",
                company: comp ? comp.innerText.trim() : "",
                links: links,
                buttons: buttons
            });
        }
    });
    return JSON.stringify(details);
})()
"""

cleaned_lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
escaped = ' '.join(cleaned_lines).replace('\\', '\\\\').replace('"', '\\"')

ascript = f'''
tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (URL of t as string) contains "foundit.in/srp" then
                return (execute t javascript "{escaped}")
            end if
        end repeat
    end repeat
    return "NO_TAB"
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("CARD DETAILS:", out)
if err: print("ERR:", err)
