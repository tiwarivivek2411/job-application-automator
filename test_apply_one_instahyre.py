from test_ascript import run_js
import time

open_js = """
(() => {
    const links = Array.from(document.querySelectorAll('a[ng-click*="openApplyModal"]'));
    if (links.length > 0) {
        links[0].click();
        return 'OPENED: ' + links[0].innerText.split('\n')[0];
    }
    return 'NO_LINKS';
})()
"""
res = run_js(open_js, "instahyre.com")
print(res[0])
time.sleep(2.0)

click_apply_js = """
(() => {
    const wrap = document.querySelector('.application-modal-wrap');
    if (!wrap) return 'NO_WRAP';
    const applyBtn = Array.from(wrap.querySelectorAll('button'))
        .find(b => b.offsetWidth > 0 && b.innerText.trim().toLowerCase() === 'apply');
    if (applyBtn) {
        applyBtn.click();
        return 'CLICKED';
    }
    return 'NO_BTN';
})()
"""
res = run_js(click_apply_js, "instahyre.com")
print("APPLY CLICK:", res[0])
time.sleep(3.0)

# Check modal state after apply
check_after = """
(() => {
    const wrap = document.querySelector('.application-modal-wrap');
    if (!wrap) return 'MODAL_CLOSED_AUTOMATICALLY';
    const btns = Array.from(wrap.querySelectorAll('button')).filter(b => b.offsetWidth > 0).map(b => b.innerText.trim());
    const text = wrap.innerText.slice(0, 100);
    return JSON.stringify({btns, text});
})()
"""
res = run_js(check_after, "instahyre.com")
print("MODAL AFTER:", res[0])

# Close modal if open
close_js = """
(() => {
    const c = document.querySelector('.application-modal-close');
    if (c) { c.click(); return 'CLOSED'; }
    return 'NO_CLOSE';
})()
"""
res = run_js(close_js, "instahyre.com")
print("CLOSE:", res[0])
