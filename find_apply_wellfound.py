from run_wellfound_js import run_js

js = """
(() => {
    const all = Array.from(document.querySelectorAll('*'));
    const found = [];
    for (const el of all) {
        if (el.innerText && el.innerText.includes('Apply on Wellfound')) {
            found.push({
                tag: el.tagName,
                cls: el.className,
                childrenCount: el.children.length,
                text: el.innerText.slice(0, 50).replace(/\\n/g, ' ')
            });
        }
    }
    return JSON.stringify(found.slice(-5));
})()
"""
out, _ = run_js(js)
print(out)
