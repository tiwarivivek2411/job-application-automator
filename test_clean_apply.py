from test_ascript import run_js
import time

open_js = """
(() => {
    const blocks = Array.from(document.querySelectorAll('.employer-block'));
    if (blocks.length === 0) return 'NO_BLOCKS';
    const b = blocks[0];
    const link = b.querySelector('a[ng-click*="openApplyModal"]');
    if (!link) return 'NO_LINK';
    link.click();
    return 'OPENED: ' + b.innerText.split('\n')[0];
})()
"""
out, _ = run_js(open_js, "instahyre.com")
print(out)
time.sleep(2.5)

apply_js = """
(() => {
    const wrap = document.querySelector('.application-modal-wrap');
    if (!wrap) return 'NO_MODAL';
    const text = wrap.innerText || '';
    if (text.includes('Application Sent')) return 'ALREADY_SENT';
    if (text.includes('Share  on social profile')) return 'ALREADY_SUBMITTED';

    const applyBtn = Array.from(wrap.querySelectorAll('button'))
        .find(b => b.offsetWidth > 0 && b.innerText.trim().toLowerCase() === 'apply');
    if (applyBtn) {
        applyBtn.click();
        return 'CLICKED_APPLY';
    }

    const extBtn = Array.from(wrap.querySelectorAll('button, a'))
        .find(b => b.offsetWidth > 0 && b.innerText.trim().toLowerCase().includes('apply on company site'));
    if (extBtn) return 'EXTERNAL_REDIRECT';

    return 'UNKNOWN_MODAL';
})()
"""
out, _ = run_js(apply_js, "instahyre.com")
print("APPLY RESULT:", out)
time.sleep(2.0)

close_js = """
(() => {
    const c = document.querySelector('.application-modal-close') || document.querySelector('.close');
    if (c) { c.click(); return 'CLOSED'; }
    return 'NO_CLOSE';
})()
"""
out, _ = run_js(close_js, "instahyre.com")
print("CLOSE RESULT:", out)
