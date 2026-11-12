from test_ascript import run_js
import time

open_js = """
(() => {
    const b = document.querySelector('.employer-block');
    const link = b?.querySelector('a[ng-click*="openApplyModal"]');
    if (link) { link.click(); return 'OPENED'; }
    return 'NO_LINK';
})()
"""
print("OPEN:", run_js(open_js, "instahyre.com")[0])
time.sleep(2.0)

inspect_js = """
(() => {
    const wrap = document.querySelector('.application-modal-wrap');
    if (!wrap) return 'NO_WRAP';
    const allBtns = Array.from(wrap.querySelectorAll('button, a.btn, input[type="submit"]'))
        .filter(b => b.offsetWidth > 0)
        .map(b => ({tag: b.tagName, text: b.innerText.trim(), cls: b.className, disabled: b.disabled}));
    const forms = Array.from(wrap.querySelectorAll('form, input, select, textarea'))
        .map(i => ({tag: i.tagName, type: i.type, name: i.name, value: i.value}));
    return JSON.stringify({allBtns, forms});
})()
"""
print("INSPECT:", run_js(inspect_js, "instahyre.com")[0])

close_js = """
(() => {
    const c = document.querySelector('.application-modal-close');
    if (c) { c.click(); return 'CLOSED'; }
    return 'NO_CLOSE';
})()
"""
print("CLOSE:", run_js(close_js, "instahyre.com")[0])
