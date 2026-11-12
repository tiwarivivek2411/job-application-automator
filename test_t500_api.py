import subprocess
import urllib.parse
import json
import requests

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_chrome_js(js_code, filter_url="talent500.com/joblist"):
    cleaned_lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
    escaped = ' '.join(cleaned_lines).replace('\\', '\\\\').replace('"', '\\"')
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "{filter_url}" then
                    return (execute t javascript "{escaped}")
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    out, err = exec_ascript(ascript)
    if err:
        print("ERR:", err)
    return out

# Extract cookie
cookie_raw = run_chrome_js("(() => encodeURIComponent(document.cookie))()")
cookie_str = urllib.parse.unquote(cookie_raw)

cookies = dict(item.strip().split("=", 1) for item in cookie_str.split(";") if "=" in item)
auth_token = cookies.get("authToken")
if auth_token:
    auth_token = urllib.parse.unquote(auth_token)

print("Auth Token prefix:", auth_token[:30] if auth_token else "NONE")

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://talent500.com",
    "Referer": "https://talent500.com/"
}
if auth_token:
    headers["Authorization"] = auth_token

url = "https://prod-warmachine.talent500.co/api/v3/jobs/search/?search_term=Software+Engineer&offset=0&limit=5&is_leadership_job=false"
r = requests.get(url, headers=headers)
print("Status code:", r.status_code)
print("Response text sample:", r.text[:500])
