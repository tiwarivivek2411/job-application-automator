from inspect_wellfound_tab import run_js
import time

click_js = """
(() => {
    const btn = document.querySelector('.styles_applyButton__7gnpI');
    if (!btn) return 'NO_BTN';
    btn.click();
    return 'CLICKED';
})()
"""
print("CLICK:", run_js(click_js)[0])
time.sleep(2.5)

check_js = """
(() => {
    const modals = Array.from(document.querySelectorAll('[role="dialog"], [class*="modal"], [class*="drawer"]'));
    const textareas = Array.from(document.querySelectorAll('textarea')).map(t => ({placeholder: t.placeholder, name: t.name}));
    const buttons = Array.from(document.querySelectorAll('button')).filter(b => b.offsetWidth > 0).map(b => b.innerText.trim()).filter(Boolean);
    return JSON.stringify({
        modalsCount: modals.length,
        textareas,
        buttons: buttons.slice(-10)
    });
})()
"""
print("AFTER CLICK:", run_js(check_js)[0])
