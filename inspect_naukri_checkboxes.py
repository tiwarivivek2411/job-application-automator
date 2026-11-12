from inspect_naukri import run_js

js = """
(() => {
    const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"], .checkbox-wrap, [class*="checkbox"]'));
    return JSON.stringify(checkboxes.map(c => ({
        tag: c.tagName,
        type: c.type,
        checked: c.checked,
        cls: c.className,
        id: c.id
    })));
})()
"""

out, _ = run_js(js)
print(out)
