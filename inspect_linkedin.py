from test_ascript import run_js
import json

js = """
(() => {
    const res = {};
    res.url = window.location.href;
    res.applyBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText && b.innerText.toLowerCase().includes('easy apply')).map(b => b.className);
    res.jobLinks = Array.from(document.querySelectorAll('a[href*="/jobs/view/"]')).length;
    res.items = Array.from(document.querySelectorAll('.scaffold-layout__list-container li, .jobs-search-results-list li')).length;
    return JSON.stringify(res);
})()
"""
out, err = run_js(js, "linkedin.com")
print("OUT:", out)
print("ERR:", err)
