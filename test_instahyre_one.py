from test_ascript import run_js
import time

check_open = """
(() => {
    const links = Array.from(document.querySelectorAll('a[ng-click*="openApplyModal"]'));
    if (links.length > 0) {
        const title = links[0].innerText.split('\\n')[0];
        links[0].click();
        return 'CLICKED_FIRST: ' + title;
    }
    return 'NO_LINKS';
})()
"""
out, err = run_js(check_open, "instahyre.com")
print("OPEN RES:", out, err)

time.sleep(2.5)

check_modal = """
(() => {
    const wrap = document.querySelector('.application-modal-wrap');
    if (!wrap) return 'NO_MODAL';

    const btns = Array.from(wrap.querySelectorAll('button'))
        .filter(b => b.offsetWidth > 0)
        .map(b => b.innerText.trim());

    return 'MODAL_BUTTONS: ' + JSON.stringify(btns);
})()
"""
out, err = run_js(check_modal, "instahyre.com")
print("MODAL RES:", out, err)

# Close modal
close_modal = """
(() => {
    const c = document.querySelector('.application-modal-close');
    if (c) { c.click(); return 'CLOSED'; }
    return 'NO_CLOSE';
})()
"""
out, err = run_js(close_modal, "instahyre.com")
print("CLOSE RES:", out, err)
