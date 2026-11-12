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
out, _ = run_js(submit_js)
print("SUBMIT:", out)
time.sleep(3.5)

check_js = """
(() => {
    const textSnippet = document.body.innerText.slice(0, 200).replace(/\\n/g, '  ');
    return textSnippet;
})()
"""
print("AFTER SUBMISSION:", run_js(check_js)[0])
