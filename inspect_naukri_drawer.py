from inspect_naukri import run_js

js = """
(() => {
    const drawer = document.querySelector('.drawer, [class*="drawer"], [role="dialog"], .chatbot, .apply-message, .applyModal');
    if (!drawer) return 'NO_DRAWER';
    const text = drawer.innerText.slice(0, 400).replace(/\\n/g, '  ');
    const buttons = Array.from(drawer.querySelectorAll('button, a')).map(b => b.innerText.trim()).filter(Boolean);
    const inputs = Array.from(drawer.querySelectorAll('input, select, textarea')).map(i => ({type: i.type, name: i.name, value: i.value}));
    return JSON.stringify({text, buttons, inputs});
})()
"""

out, _ = run_js(js)
print(out)
