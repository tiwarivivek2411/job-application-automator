import subprocess
import urllib.parse
import json

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

code = """
(() => {
    let cards = [];
    document.querySelectorAll('a').forEach(a => {
        let t = a.innerText.replace(/\\n/g, ' -- ').trim();
        if (t.length > 20 && (a.href.includes('/job') || a.href.includes('/company') || a.href.includes('paypay') || a.href.includes('relocate'))) {
            cards.push({href: a.href, text: t});
        }
    });
    let loginLink = Array.from(document.querySelectorAll('a')).find(a => a.innerText.toLowerCase().includes('login') || a.innerText.toLowerCase().includes('sign'));
    return encodeURIComponent(JSON.stringify({
        cardsCount: cards.length,
        cards: cards.slice(0, 10),
        loginHref: loginLink ? loginLink.href : null
    }));
})()
"""

cleaned = ' '.join([l.strip() for l in code.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
ascript = f'''
tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (URL of t as string) contains "relocate.me" then
                return (execute t javascript "{cleaned}")
            end if
        end repeat
    end repeat
    return "NO_TAB"
end tell
'''
out, _ = exec_ascript(ascript)
print(urllib.parse.unquote(out))
