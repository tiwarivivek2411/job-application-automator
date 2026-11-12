from run_wellfound_js import run_js
import time

click_js = """
(() => {
    const btn = Array.from(document.querySelectorAll('button'))
        .find(b => b.innerText && b.innerText.trim().toLowerCase() === 'apply now');
    if (!btn) return 'NO_APPLY_NOW';
    btn.click();
    return 'CLICKED_APPLY_NOW';
})()
"""
out, _ = run_js(click_js)
print("CLICK:", out)
time.sleep(3.0)

modal_js = """
(() => {
    const modal = document.querySelector('[role="dialog"], [data-test-modal], .styles_modalContent__');
    const allBtns = Array.from(document.querySelectorAll('button, a.btn, input[type="submit"]'))
        .map(b => b.innerText.trim().replace(/\\n/g, ' ')).filter(Boolean);
    const inputs = Array.from(document.querySelectorAll('textarea, input'))
        .map(i => ({type: i.type, name: i.name, placeholder: i.placeholder, value: i.value}));
    const textSnippet = document.body.innerText.slice(0, 300).replace(/\\n/g, '  ');
    return JSON.stringify({allBtns, inputs, textSnippet});
})()
"""
out, _ = run_js(modal_js)
print("MODAL:", out)
