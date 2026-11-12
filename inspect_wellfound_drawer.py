from run_wellfound_js import run_js

js = """
(() => {
    const candidates = Array.from(document.querySelectorAll('div, section, aside'))
        .filter(el => {
            const t = el.innerText || '';
            return t.includes('Hiring Full Time Remote Python Developers') && el.children.length > 2;
        });
    if (candidates.length === 0) return 'NO_CANDIDATES';
    const drawer = candidates[candidates.length - 1];
    const buttons = Array.from(drawer.querySelectorAll('button, a')).map(b => b.innerText.trim().replace(/\\n/g, ' ')).filter(Boolean);
    return JSON.stringify({
        tag: drawer.tagName,
        cls: drawer.className,
        buttons: buttons.slice(0, 15)
    });
})()
"""
out, _ = run_js(js)
print(out)
