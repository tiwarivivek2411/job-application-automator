from run_wellfound_js import run_js
import time

click_js = """
(() => {
    const btn = document.querySelector('.styles_applyButton__7gnpI') || 
                Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase() === 'apply');
    if (!btn) return 'NO_APPLY_BTN';
    btn.click();
    return 'CLICKED_REAL_APPLY';
})()
"""
print("CLICK:", run_js(click_js)[0])
time.sleep(3.0)

inspect_js = """
(() => {
    // Check for modal or application form
    const form = document.querySelector('form, textarea, [class*="modal"], [class*="drawer"]');
    const allBtns = Array.from(document.querySelectorAll('button'))
        .filter(b => b.offsetWidth > 0)
        .map(b => b.innerText.trim().replace(/\\n/g, ' '));
    const textarea = document.querySelector('textarea');
    return JSON.stringify({
        hasForm: !!form,
        hasTextarea: !!textarea,
        buttons: allBtns.slice(-10)
    });
})()
"""
print("INSPECT AFTER APPLY:", run_js(inspect_js)[0])
