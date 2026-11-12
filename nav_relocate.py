import subprocess
import time

script = '''
tell application "Google Chrome"
    set t to tab 21 of front window
    set URL of t to "https://relocate.me/jobs"
    return "NAVIGATED"
end tell
'''
p = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
print(p.stdout)
