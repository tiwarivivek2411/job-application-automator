from inspect_naukri import run_js
import time

select_js = """
(() => {
    function isSoftwareRole(title) {
        if (!title) return false;
        const t = title.toLowerCase();
        const blocked = ['sales', 'marketing', 'product owner', 'product manager', 'hr', 'recruiter', 'business analyst'];
        if (blocked.some(b => t.includes(b))) return false;
        const allowed = ['software', 'developer', 'backend', 'full stack', 'fullstack', 'devops', 'sde', 'engineer', 'architect'];
        return allowed.some(a => t.includes(a));
    }

    const articles = Array.from(document.querySelectorAll('article.jobTuple'));
    let selected = 0;
    const selectedList = [];

    for (const art of articles) {
        if (selected >= 5) break;
        const titleEl = art.querySelector('a.title, .title');
        const title = titleEl ? titleEl.innerText.trim() : '';
        const comp = art.querySelector('.comp-name, [class*="comp-name"]')?.innerText.trim() || '';
        
        if (isSoftwareRole(title)) {
            const cb = art.querySelector('input.tuple-check-input');
            const label = art.querySelector('label.tuple-check-box');
            if (cb && !cb.checked && label) {
                label.click();
                selected++;
                selectedList.push(title + ' @ ' + comp);
            } else if (cb && cb.checked) {
                selected++;
                selectedList.push(title + ' @ ' + comp + ' (already checked)');
            }
        }
    }

    return JSON.stringify({
        selected,
        selectedList,
        btnDisabled: document.querySelector('.multi-apply-button')?.disabled
    });
})()
"""

out, _ = run_js(select_js)
print("SELECT RESULT:", out)
time.sleep(2.0)

# Click Apply
click_apply_js = """
(() => {
    const btn = document.querySelector('.multi-apply-button');
    if (!btn || btn.disabled) return 'CANNOT_CLICK';
    btn.click();
    return 'CLICKED_MULTI_APPLY';
})()
"""
out, _ = run_js(click_apply_js)
print("APPLY CLICK:", out)
time.sleep(3.5)

# Inspect what happened
check_after_js = """
(() => {
    const drawer = document.querySelector('.drawer, [class*="drawer"], [role="dialog"], .chatbot, .apply-message');
    const toast = document.querySelector('.toast, .snackbar, [class*="success"], [class*="alert"]')?.innerText || '';
    const textSnippet = document.body.innerText.slice(0, 300).replace(/\\n/g, '  ');
    return JSON.stringify({
        hasDrawer: !!drawer,
        drawerText: drawer ? drawer.innerText.slice(0, 200).replace(/\\n/g, ' ') : '',
        toast,
        textSnippet: textSnippet.slice(0, 150)
    });
})()
"""
out, _ = run_js(check_after_js)
print("AFTER APPLY:", out)
