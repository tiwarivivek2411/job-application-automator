from inspect_wellfound_tab import run_js

js = """
(() => {
    const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
    if (cancelBtn) {
        cancelBtn.click();
        return 'CLICKED_CANCEL';
    }
    return 'NO_CANCEL';
})()
"""
out, _ = run_js(js)
print(out)
