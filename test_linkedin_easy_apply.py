from test_ascript import run_js
import time

click_js = """
(() => {
    const btn = Array.from(document.querySelectorAll('button'))
        .find(b => b.innerText && b.innerText.toLowerCase().includes('easy apply'));
    if (!btn) return 'NO_BTN';
    btn.click();
    return 'CLICKED_EASY_APPLY';
})()
"""
out, _ = run_js(click_js, "linkedin.com")
print("CLICK:", out)
time.sleep(2.5)

modal_js = """
(() => {
    const modal = document.querySelector('.jobs-easy-apply-modal, [data-test-modal], [role="dialog"]');
    if (!modal) return 'NO_MODAL';
    const text = modal.innerText.replace(/\\n/g, ' ').slice(0, 300);
    const buttons = Array.from(modal.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
    const inputs = Array.from(modal.querySelectorAll('input, select, textarea')).map(i => ({
        type: i.type,
        name: i.name,
        id: i.id,
        value: i.value,
        label: i.closest('div')?.innerText?.slice(0, 50)?.replace(/\\n/g, ' ') || ''
    }));
    return JSON.stringify({text, buttons, inputs});
})()
"""
out, _ = run_js(modal_js, "linkedin.com")
print("MODAL:", out)
