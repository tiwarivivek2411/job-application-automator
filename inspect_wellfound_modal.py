from run_wellfound_js import run_js

js = """
(() => {
    const modal = document.querySelector('[role="dialog"]');
    if (!modal) return 'NO_MODAL';
    const buttons = Array.from(modal.querySelectorAll('button, a')).map(b => ({
        tag: b.tagName,
        text: b.innerText.trim().replace(/\\n/g, ' '),
        cls: b.className
    })).filter(b => b.text.length > 0 && b.text.length < 50);
    const title = modal.querySelector('h1, h2, h3, h4')?.innerText || '';
    return JSON.stringify({title, buttons});
})()
"""
out, _ = run_js(js)
print(out)
