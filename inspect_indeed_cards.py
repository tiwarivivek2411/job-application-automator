import subprocess
import json

def get_indeed_cards():
    ascript = '''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "indeed.com/jobs" then
                    return (execute t javascript "(() => {
                        const cards = Array.from(document.querySelectorAll('.job_seen_beacon, .result, [data-jk]')).map(c => {
                            const titleEl = c.querySelector('h2.jobTitle, a[data-jk], [class*=\\"jobTitle\\"]');
                            const compEl = c.querySelector('[data-testid=\\"company-name\\"], .companyName');
                            const isEasy = c.innerText.includes('Easily apply');
                            const jk = c.getAttribute('data-jk') || c.querySelector('a[data-jk]')?.getAttribute('data-jk');
                            return {
                                jk: jk,
                                title: titleEl ? titleEl.innerText.trim() : '',
                                company: compEl ? compEl.innerText.trim() : '',
                                isEasy: isEasy
                            };
                        }).filter(c => c.title);
                        return JSON.stringify(cards);
                    })()")
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=ascript.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

out, err = get_indeed_cards()
print("OUT:", out)
if err: print("ERR:", err)
