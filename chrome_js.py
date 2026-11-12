import subprocess
import base64
import json
import sys

def run_js_on_tab(js_code, filter_url=None, tab_id=None):
    b64 = base64.b64encode(js_code.encode('utf-8')).decode('ascii')
    if tab_id is not None:
        ascript = f'''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    if (id of t as string) is "{tab_id}" then
                        return (execute t javascript "eval(atob('{b64}'))")
                    end if
                end repeat
            end repeat
            return "NO_TAB"
        end tell
        '''
    else:
        ascript = f'''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    if (URL of t as string) contains "{filter_url}" then
                        return (execute t javascript "eval(atob('{b64}'))")
                    end if
                end repeat
            end repeat
            return "NO_TAB"
        end tell
        '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=ascript.encode('utf-8'))
    return out.decode('utf-8').strip()

if __name__ == '__main__':
    filter_arg = sys.argv[1] if len(sys.argv) > 1 else "linkedin.com/jobs"
    code = sys.argv[2] if len(sys.argv) > 2 else "document.title"
    print(run_js_on_tab(code, filter_url=filter_arg))
