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
time.sleep(3.0)

inspect_js = """
(() => {
    const wrap = document.querySelector('.application-modal-wrap') || document.querySelector('.modal-content') || document.querySelector('[role="dialog"]');
    if (!wrap) return 'NO_WRAP_OR_MODAL';
    return JSON.stringify({
        wrap_class: wrap.className,
        visible_text: wrap.innerText.slice(0, 300),
        buttons: Array.from(wrap.querySelectorAll('button')).map(b => ({text: b.innerText.trim(), visible: b.offsetWidth > 0, cls: b.className}))
    });
})()
"""
print("INSPECT:", run_js(inspect_js, "instahyre.com")[0])

close_js = """
(() => {
    const c = document.querySelector('.application-modal-close') || document.querySelector('.close');
    if (c) { c.click(); return 'CLOSED'; }
    return 'NO_CLOSE';
})()
"""
print("CLOSE:", run_js(close_js, "instahyre.com")[0])
