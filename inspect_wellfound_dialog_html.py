from run_wellfound_js import run_js

js = """
(() => {
    const d = document.querySelector('[role="dialog"]');
    if (!d) return 'NO_DIALOG';
    return JSON.stringify({
        cls: d.className,
        text: d.innerText.slice(0, 300).replace(/\\n/g, '  ')
    });
})()
"""
out, _ = run_js(js)
print(out)
