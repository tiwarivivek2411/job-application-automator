import subprocess
import json

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

code = """
(() => {
    // Find all job listings on the page
    let links = [];
    document.querySelectorAll('a').forEach(a => {
        if (a.href && (a.href.includes('/jobs/') || a.href.includes('jobId='))) {
            let title = a.innerText.trim().replace(/\\n/g, ' -- ');
            if (title.length > 5 && !links.some(l => l.href === a.href)) {
                links.push({href: a.href, text: title});
            }
        }
    });
    
    // Check if there are company cards
    let companies = [];
    document.querySelectorAll('div').forEach(d => {
        if (d.className && typeof d.className === 'string' && d.className.includes('companyCard')) {
            companies.push(d.innerText.slice(0, 100).replace(/\\n/g, ' '));
        }
    });

    return JSON.stringify({linksCount: links.length, links: links.slice(0, 15), companies: companies.slice(0, 5)});
})()
"""

cleaned = ' '.join([l.strip() for l in code.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
ascript = f'''
tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (URL of t as string) contains "levels.fyi/jobs" then
                return (execute t javascript "{cleaned}")
            end if
        end repeat
    end repeat
    return "NO_TAB"
end tell
'''
out, _ = exec_ascript(ascript)
print(out)
