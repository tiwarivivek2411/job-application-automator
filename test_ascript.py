import subprocess

def run_js(js_code, filter_url):
    escaped = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
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

js = """
(() => {
    const a = Array.from(document.querySelectorAll('a[ng-click*="openApplyModal"]'));
    return 'FOUND_A: ' + a.length;
})()
"""

out, err = run_js(js, "instahyre.com")
print("OUT:", out)
print("ERR:", err)
