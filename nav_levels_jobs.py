import subprocess
import time

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

# Navigate Tab 7 to Levels.fyi jobs
ascript = '''
tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (URL of t as string) contains "levels.fyi" then
                set URL of t to "https://www.levels.fyi/jobs?jobFamily=software-engineer"
                return "NAVIGATED"
            end if
        end repeat
    end repeat
    return "NO_TAB"
end tell
'''
print(exec_ascript(ascript))
