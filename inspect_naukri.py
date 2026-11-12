import subprocess, json

js_code = """
(function() {
    var tuples = document.querySelectorAll(".jobTuple, .srp-jobtuple-wrapper, article.jobTuple, div[data-job-id]");
    var list = [];
    tuples.forEach(function(t, idx) {
        var title = t.querySelector("a.title, .job-title, [class*='title']");
        var comp = t.querySelector("a.subTitle, .comp-name, [class*='company']");
        var cb = t.querySelector("input[type='checkbox'], .checkbox-wrap input");
        var applied = t.querySelector(".applied, .applied-tag, [class*='already-applied']");
        if (title) {
            list.push({
                index: idx,
                title: title.innerText.trim(),
                company: comp ? comp.innerText.trim() : "",
                hasCheckbox: !!cb,
                checked: cb ? cb.checked : false,
                applied: applied ? applied.innerText.trim() : "no"
            });
        }
    });
    var multiBtn = document.querySelector(".multi-apply-button, [class*='multiApply'], button[id*='apply']");
    return JSON.stringify({
        total: list.length,
        jobs: list.slice(0, 15),
        multiBtn: multiBtn ? multiBtn.innerText.trim() : "none"
    });
})()
"""

escaped_js = js_code.replace('\n', ' ').replace('"', '\\"')
apple_script = 'tell application "Google Chrome"\n' \
               '    tell (first tab of window 1 whose id is 33684098)\n' \
               f'        return execute javascript "{escaped_js}"\n' \
               '    end tell\n' \
               'end tell'

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(apple_script)
print("NAUKRI JOBS:", out)
if err: print("ERR:", err)
