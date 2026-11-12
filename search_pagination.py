import requests
import re

# List of bundle scripts from earlier
urls = [
    "https://talent500.com/wp-content/plugins/t500-apply/wp-build/Jobs.d6011651989a55402aa8.js",
    "https://talent500.com/wp-content/plugins/t500-apply/wp-build/jobs-widgets.d6011651989a55402aa8.js",
    "https://talent500.com/wp-content/plugins/t500-apply/wp-build/2784.d6011651989a55402aa8.js",
    "https://talent500.com/wp-content/plugins/t500-apply/wp-build/JD-new.d6011651989a55402aa8.js",
    "https://talent500.com/wp-content/plugins/t500-apply/wp-build/companyJobsPage.d6011651989a55402aa8.js"
]

for u in urls:
    r = requests.get(u, headers={"User-Agent": "Mozilla/5.0"})
    matches = [m.start() for m in re.finditer(r'v3/jobs/search', r.text)]
    if matches:
        print(f"File {u.split('/')[-1]} has {len(matches)} matches:")
        for idx in matches:
            print("  ", r.text[max(0, idx-60):min(len(r.text), idx+140)])
