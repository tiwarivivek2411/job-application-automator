from inspect_linkedin_view import run_js
import time

url = "https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED"
run_js(f'window.location.href = "{url}"')
time.sleep(4.0)

js = """
(() => {
    return JSON.stringify({
        url: window.location.href,
        title: document.title,
        text: document.body.innerText.slice(0, 3000)
    });
})()
"""

out, _ = run_js(js)
print(out)
