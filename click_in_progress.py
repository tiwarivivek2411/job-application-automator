from inspect_linkedin_view import run_js
import time

js = """
(() => {
    const labels = Array.from(document.querySelectorAll('label')).filter(l => l.innerText && l.innerText.includes('In Progress'));
    if (labels.length > 0) {
        labels[0].click();
        return 'CLICKED_IN_PROGRESS';
    }
    return 'NO_LABEL';
})()
"""
out, _ = run_js(js)
print(out)
time.sleep(3.0)

check = """
(() => {
    return document.body.innerText.slice(0, 1500).replace(/\\n/g, '  ');
})()
"""
print(run_js(check)[0])
