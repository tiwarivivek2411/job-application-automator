from inspect_wellfound_tab import run_js
import time

submit_js = """
(() => {
    const btn = Array.from(document.querySelectorAll('button'))
        .find(b => b.offsetWidth > 0 && b.innerText.trim().toLowerCase() === 'send application');
    if (!btn) return 'NO_SEND_BTN';
    btn.click();
    return 'CLICKED_SEND_APPLICATION';
})()
"""
print("SUBMIT:", run_js(submit_js)[0])
time.sleep(3.5)

check_js = """
(() => {
    const textSnippet = document.body.innerText.slice(0, 300).replace(/\\n/g, '  ');
    const allBtns = Array.from(document.querySelectorAll('button')).filter(b => b.offsetWidth > 0).map(b => b.innerText.trim());
    return JSON.stringify({
        buttons: allBtns.slice(-8),
        textSnippet: textSnippet.slice(0, 150)
    });
})()
"""
print("AFTER SUBMISSION:", run_js(check_js)[0])
