import subprocess, json

js_code = """
(function() {
    var cards = document.querySelectorAll(".srpResultCard, .cardContainer, div[class*='cardContainer'], div[class*='srpResultCard']");
    var res = [];
    cards.forEach(function(c, idx) {
        var t = c.querySelector(".jobTitle, [class*='jobTitle'], h3, a[href*='job-desc']");
        var comp = c.querySelector(".companyName, [class*='companyName']");
        var btn = c.querySelector("button, .applyBtnCont, [class*='apply']");
        if (t) {
            res.push({
                index: idx,
                title: t.innerText.trim(),
                company: comp ? comp.innerText.trim() : "",
                btn: btn ? btn.innerText.trim() : "none"
            });
        }
    });
    return JSON.stringify(res);
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
print("OUT:", out)
if err: print("ERR:", err)
