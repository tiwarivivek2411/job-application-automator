import subprocess
import time
import json

def run_js(js_code, filter_url="linkedin.com"):
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
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=ascript.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

# Let's inspect the list of jobs on LinkedIn
js = """
(() => {
    const links = Array.from(document.querySelectorAll('a[href*="/jobs/view/"], [data-job-id] a')).map(a => ({
        href: a.href,
        text: a.innerText.replace(/\\n/g, ' ').slice(0, 100)
    })).filter(a => a.text.length > 5);
    return JSON.stringify({
        url: window.location.href,
        title: document.title,
        jobLinks: links.slice(0, 15)
    });
})()
"""

out, _ = run_js(js)
print(out)
