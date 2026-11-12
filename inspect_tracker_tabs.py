from inspect_linkedin_view import run_js
import time

js = """
(() => {
    // Click Applied tab or In Progress tab
    const tabs = Array.from(document.querySelectorAll('a, button')).filter(e => e.innerText && (e.innerText.includes('Applied') || e.innerText.includes('In Progress')));
    const appliedTab = tabs.find(t => t.innerText.includes('Applied'));
    if (appliedTab) {
        appliedTab.click();
        return 'CLICKED_APPLIED_TAB';
    }
    return 'NO_TAB';
})()
"""
out, _ = run_js(js)
print("CLICK TAB:", out)
time.sleep(3.5)

check_js = """
(() => {
    return JSON.stringify({
        url: window.location.href,
        text: document.body.innerText.slice(0, 3000)
    });
})()
"""
out, _ = run_js(check_js)
print("APPLIED JOBS:", out)
