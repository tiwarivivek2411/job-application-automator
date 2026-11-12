from inspect_wellfound_tab import run_js
import time

click_js = """
(() => {
    const btn = document.querySelector('.styles_applyButton__7gnpI');
    if (!btn) return 'NO_BTN';
    btn.click();
    return 'CLICKED_APPLY';
})()
"""
print("APPLY CLICK:", run_js(click_js)[0])
time.sleep(2.5)

inspect_modal = """
(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Send application');
    if (!btn) return 'NO_SEND_BTN';
    let p = btn.parentElement;
    for (let i = 0; i < 6 && p; i++) {
        if (p.innerText && p.innerText.length > 20) {
            const inputs = Array.from(p.querySelectorAll('input, textarea, select')).map(i => ({
                tag: i.tagName,
                type: i.type,
                placeholder: i.placeholder,
                required: i.required,
                label: i.closest('div')?.innerText?.slice(0, 50)?.replace(/\\n/g, ' ') || ''
            }));
            return JSON.stringify({text: p.innerText.replace(/\\n/g, '  '), inputs});
        }
        p = p.parentElement;
    }
    return 'NO_CONTAINER';
})()
"""
print("MODAL:", run_js(inspect_modal)[0])
