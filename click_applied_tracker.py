from inspect_linkedin_view import run_js
import time

js = """
(() => {
    const labels = Array.from(document.querySelectorAll('label')).filter(l => l.innerText && l.innerText.includes('Applied'));
    if (labels.length > 0) {
        labels[0].click();
        return 'CLICKED_APPLIED_LABEL';
    }
    return 'NO_LABEL';
})()
"""
out, _ = run_js(js)
print(out)
time.sleep(3.0)

check = """
(() => {
    const items = Array.from(document.querySelectorAll('li, tr, [class*="item"], [class*="card"]'))
        .filter(e => e.innerText && e.innerText.includes('Applied'))
        .map(e => e.innerText.slice(0, 100).replace(/\\n/g, ' '));
    return JSON.stringify(items.slice(0, 10));
})()
"""
out, _ = run_js(check)
print(out)
