from test_ascript import run_js
import json

js = """
(() => {
    const res = {};
    res.url = window.location.href;
    res.title = document.title;
    res.applyBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText && b.innerText.toLowerCase().includes('apply')).map(b => b.innerText);
    res.jobs = Array.from(document.querySelectorAll('[data-test="JobListing"]')).length;
    res.allButtons = Array.from(document.querySelectorAll('button')).slice(0, 10).map(b => b.innerText.trim());
    return JSON.stringify(res);
})()
"""
out, err = run_js(js, "wellfound.com")
print("OUT:", out)
print("ERR:", err)
