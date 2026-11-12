from test_ascript import run_js

js = """
(() => {
    const textSnippets = Array.from(document.querySelectorAll('a, button, div'))
        .filter(e => e.innerText && (e.innerText.toLowerCase().includes('apply') || e.innerText.toLowerCase().includes('learn more')))
        .slice(0, 10)
        .map(e => ({tag: e.tagName, text: e.innerText.slice(0, 50), cls: e.className}));
    return JSON.stringify(textSnippets);
})()
"""
out, err = run_js(js, "wellfound.com")
print("OUT:", out)
