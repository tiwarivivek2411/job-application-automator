from inspect_linkedin_view import run_js
import time

js = """
(() => {
    const btn = Array.from(document.querySelectorAll('button'))
        .find(b => b.offsetWidth > 0 && b.innerText && b.innerText.toLowerCase().includes('easy apply'));
    if (!btn) return 'NO_BTN';
    
    // Check if there is an inner clickable span or svg
    const span = Array.from(btn.querySelectorAll('span')).find(s => s.innerText.trim() === 'Easy Apply');
    if (span) {
        span.click();
        return 'CLICKED_SPAN';
    }
    btn.click();
    return 'CLICKED_BTN';
})()
"""
out, _ = run_js(js)
print("CLICK:", out)
time.sleep(2.0)

check_js = """
(() => {
    const dialogs = Array.from(document.querySelectorAll('*')).filter(el => {
        return (el.getAttribute('role') === 'dialog' || el.getAttribute('aria-modal') === 'true');
    });
    return 'DIALOGS: ' + dialogs.length;
})()
"""
out, _ = run_js(check_js)
print("DIALOGS:", out)
