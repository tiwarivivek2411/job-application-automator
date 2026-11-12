import subprocess, base64, time

def run_js(url_sub, js):
    b64 = base64.b64encode(js.encode('utf-8')).decode('utf-8')
    ascript = f'''
    tell application "Google Chrome"
        repeat with t in tabs of window 1
            if (URL of t as string) contains "{url_sub}" then
                return (execute t javascript "try {{ eval(atob('{b64}')); }} catch(e) {{ 'ERR: ' + e.message; }}")
            end if
        end repeat
        return "NO_TAB"
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(ascript)
    return out.strip()

# Navigate to Eltropy job
nav_js = r'''
window.location.href = "https://my.greenhouse.io/jobs/eltropyinc/4451602009?from_recommendation=true";
'''
print('Navigating:', run_js('my.greenhouse.io', nav_js))
time.sleep(3.5)

check_js = r'''
(() => {
    return JSON.stringify({
        url: window.location.href,
        title: document.title,
        applyBtns: Array.from(document.querySelectorAll('button, a')).filter(e => (e.innerText || '').toLowerCase().includes('apply')).map(e => ({ tag: e.tagName, text: e.innerText.trim(), href: e.href || '', className: e.className })),
        bodySnippet: document.body.innerText.slice(0, 400)
    });
})()
'''

print(run_js('eltropy', check_js))
