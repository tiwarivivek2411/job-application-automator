from inspect_linkedin_screener_questions import run_js

js = """
(() => {
    const p = Array.from(document.querySelectorAll('p')).find(e => e.innerText.trim() === 'Blue Machines AI');
    if (!p) return 'NO_P';
    let el = p;
    const hierarchy = [];
    while (el && el !== document.body) {
        hierarchy.push({tag: el.tagName, cls: el.className, id: el.id, href: el.getAttribute('href')});
        if (el.tagName === 'LI' || el.classList.contains('job-card-container') || el.hasAttribute('data-occludable-job-id')) {
            break;
        }
        el = el.parentElement;
    }
    return JSON.stringify(hierarchy);
})()
"""

out, _ = run_js(js)
print(out)
