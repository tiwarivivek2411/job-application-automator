from inspect_naukri import run_js
import time

js = """
(() => {
    // Select first 3 software checkboxes
    const tuples = Array.from(document.querySelectorAll('.cust-job-tuple'));
    let selected = 0;
    const selectedTitles = [];

    for (const tuple of tuples) {
        if (selected >= 5) break;
        const titleEl = tuple.querySelector('.title, a.title');
        const title = titleEl ? titleEl.innerText.trim() : '';
        
        // Software check
        const t = title.toLowerCase();
        if (t.includes('software') || t.includes('developer') || t.includes('backend') || t.includes('sde') || t.includes('engineer')) {
            const cb = tuple.querySelector('input.tuple-check-input');
            const icon = tuple.querySelector('.naukicon-ot-checkbox');
            if (cb && !cb.checked) {
                if (icon) icon.click();
                else cb.click();
                selected++;
                selectedTitles.push(title);
            }
        }
    }

    const applyBtn = Array.from(document.querySelectorAll('button, a'))
        .find(b => b.innerText && b.innerText.trim().toLowerCase() === 'apply');

    return JSON.stringify({
        selectedCount: selected,
        selectedTitles: selectedTitles,
        applyBtnText: applyBtn ? applyBtn.innerText : 'NO_BTN',
        applyBtnDisabled: applyBtn ? applyBtn.disabled : true,
        applyBtnCls: applyBtn ? applyBtn.className : ''
    });
})()
"""

out, _ = run_js(js)
print(out)
