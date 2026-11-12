from inspect_linkedin_screener_questions import run_js
import time

url = "https://www.linkedin.com/jobs/search/?keywords=Backend%20Developer&f_AL=true&location=Bengaluru%2C%20Karnataka%2C%20India"
run_js(f'window.location.href = "{url}"')
time.sleep(5.0)

check_js = """
(() => {
    const jobItems = Array.from(document.querySelectorAll('.scaffold-layout__list-container li, .jobs-search-results-list li, [data-occludable-job-id]')).map(c => {
        const title = c.querySelector('a.job-card-list__title, a[href*="/jobs/view/"], strong')?.innerText.trim() || '';
        const comp = c.querySelector('.job-card-container__primary-description, [class*="company"]')?.innerText.trim() || '';
        const link = c.querySelector('a[href*="/jobs/view/"]')?.href || '';
        return {title, comp, link};
    }).filter(j => j.title);
    return JSON.stringify({
        url: window.location.href,
        title: document.title,
        totalJobs: jobItems.length,
        jobs: jobItems.slice(0, 10)
    });
})()
"""
out, _ = run_js(check_js)
print(out)
