from inspect_wellfound_tab import run_js

js = """
(() => {
    const cards = Array.from(document.querySelectorAll('.mb-6.overflow-hidden.rounded-md')).map(card => {
        const comp = card.querySelector('h2, [class*="company"], a[href*="/company/"]')?.innerText.trim() || '';
        const title = card.querySelector('a[href*="/jobs/"]')?.innerText.split('\\n')[0].trim() || '';
        const link = card.querySelector('a[href*="/jobs/"]')?.href || '';
        const learnMoreBtn = Array.from(card.querySelectorAll('button')).some(b => b.innerText.includes('Learn more'));
        return {comp, title, link, learnMoreBtn};
    });
    return JSON.stringify(cards);
})()
"""

out, _ = run_js(js)
print(out)
