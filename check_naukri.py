import subprocess
import time

time.sleep(3.0)
ascript = '''
tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (URL of t as string) contains "naukri.com" then
                return (URL of t as string) & " --- " & (title of t as string)
            end if
        end repeat
    end repeat
    return "NO_TAB"
end tell
'''
p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, _ = p.communicate(input=ascript.encode('utf-8'))
print(out.decode('utf-8').strip())
