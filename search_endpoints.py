import requests

url = "https://talent500.com/wp-content/plugins/t500-apply/wp-build/JD-new.d6011651989a55402aa8.js"
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(url, headers=headers)

idx = r.text.find("p=await(0,h.bE)(T.rl.candidateJobs")
snippet = r.text[max(0, idx-1200):idx]
print("--- SCOPE OF o ---")
print(snippet)
