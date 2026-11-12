from run_wellfound_js import run_js
import time

js = """
(() => {
    const card = document.querySelector('.mb-6.overflow-hidden.rounded-md');
    if (!card) return 'NO_CARD';
    const btn = Array.from(card.querySelectorAll('button')).find(b => b.innerText.trim() === 'Learn more');
    if (!btn) return 'NO_BTN';
    btn.click();
    return 'CLICKED_LEARN_MORE';
})()
"""
out, _ = run_js(js)
print("CLICK:", out)
time.sleep(3.0)

check_js = """
(() => {
    const modal = document.querySelector('[role="dialog"], [data-test-modal], .styles_modal__');
    const allBtns = Array.from(document.querySelectorAll('button, a'))
        .filter(b => b.innerText && (b.innerText.toLowerCase().includes('apply') || b.innerText.toLowerCase().includes('submit')))
        .map(b => b.innerText.trim().replace(/\\n/g, ' '));
    return JSON.stringify({
        url: window.location.href,
        hasModal: !!modal,
        applyButtons: allBtns.slice(0, 10)
    });
})()
"""
out, _ = run_js(check_js)
print("AFTER CLICK:", out)
