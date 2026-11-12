from inspect_linkedin_view import run_js
import time

js = """
(() => {
    const btn = Array.from(document.querySelectorAll('button'))
        .find(b => b.offsetWidth > 0 && b.innerText && b.innerText.toLowerCase().includes('easy apply'));
    if (!btn) return 'NO_BTN';
    btn.click();
    return 'CLICKED_EASY_APPLY';
})()
"""
out, _ = run_js(js)
print("CLICK:", out)
time.sleep(3.0)

check_js = """
(() => {
    const modal = document.querySelector('[role="dialog"], [data-test-modal], .jobs-easy-apply-modal');
    if (!modal) return 'NO_MODAL';
    const text = modal.innerText.replace(/\\n/g, ' ').slice(0, 300);
    const buttons = Array.from(modal.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
    return JSON.stringify({text, buttons});
})()
"""
out, _ = run_js(check_js)
print("MODAL:", out)
