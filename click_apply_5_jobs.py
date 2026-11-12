from inspect_naukri import run_js
import time

js = """
(() => {
    const btn = Array.from(document.querySelectorAll('button, a'))
        .find(b => b.innerText && b.innerText.includes('Apply 5 Jobs'));
    if (!btn) return 'NO_APPLY_5_BTN';
    btn.click();
    return 'CLICKED_APPLY_5_JOBS';
})()
"""

out, _ = run_js(js)
print(out)
time.sleep(3.5)

check_js = """
(() => {
    const alert = document.querySelector('.toast, .snackbar, .success, [class*="success"], [class*="alert"]')?.innerText || '';
    const textSnippet = document.body.innerText.slice(0, 300).replace(/\\n/g, '  ');
    const modal = document.querySelector('[role="dialog"], .chatbot, .applyModal');
    return JSON.stringify({
        alert,
        hasModal: !!modal,
        modalText: modal ? modal.innerText.slice(0, 200).replace(/\\n/g, ' ') : '',
        textSnippet: textSnippet.slice(0, 150)
    });
})()
"""
print(run_js(check_js)[0])
