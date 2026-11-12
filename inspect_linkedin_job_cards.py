from inspect_linkedin_screener_questions import run_js

js = """
(() => {
    const all = Array.from(document.querySelectorAll('*')).filter(el => {
        return el.innerText && el.innerText.includes('Blue Machines AI');
    });
    if (all.length === 0) return 'NO_MATCH';
    const deepest = all[all.length - 1];
    return JSON.stringify({
        tag: deepest.tagName,
        cls: deepest.className,
        outer: deepest.outerHTML.slice(0, 300)
    });
})()
"""

out, _ = run_js(js)
print(out)
