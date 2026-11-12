import subprocess, json

js_code = """
(function() {
    var tuples = document.querySelectorAll(".jobTuple, .srp-jobtuple-wrapper, article.jobTuple, div[data-job-id]");
    var softwareRoles = [];
    tuples.forEach(function(t, idx) {
        var titleEl = t.querySelector("a.title, .job-title, [class*='title']");
        var compEl = t.querySelector("a.subTitle, .comp-name, [class*='company']");
        var cb = t.querySelector("input[type='checkbox'], .checkbox-wrap input");
        var applied = t.querySelector(".applied, .applied-tag, [class*='already-applied']");
        if (titleEl && cb && !applied) {
            var title = titleEl.innerText.trim();
            var comp = compEl ? compEl.innerText.trim() : "";
            softwareRoles.push({
                index: idx,
                title: title,
                company: comp,
                checkboxId: cb.id,
                jobId: t.getAttribute("data-job-id")
            });
        }
    });
    return JSON.stringify(softwareRoles);
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
print("CHECKBOX ROLES:", out)
if err: print("ERR:", err)
