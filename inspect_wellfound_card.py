from run_wellfound_js import run_js

js = """
(() => {
    const card = document.querySelector('.mb-6.overflow-hidden.rounded-md');
    if (!card) return 'NO_CARD';
    const links = Array.from(card.querySelectorAll('a')).map(a => ({href: a.href, text: a.innerText.trim(), cls: a.className}));
    const buttons = Array.from(card.querySelectorAll('button')).map(b => ({text: b.innerText.trim(), cls: b.className}));
    return JSON.stringify({links, buttons});
})()
"""
out, _ = run_js(js)
print(out)
