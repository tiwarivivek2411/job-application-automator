import subprocess
import json

applescript = """
tell application "Google Chrome"
    set windowList to every window
    set tabInfo to {}
    repeat with w in windowList
        set tabList to every tab of w
        repeat with t in tabList
            set tabTitle to title of t
            set tabURL to URL of t
            set end of tabInfo to {title:tabTitle, url:tabURL}
        end repeat
    end repeat
    return tabInfo
end tell
"""

try:
    # Run the apple script
    proc = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
    if proc.returncode != 0:
        print("Error running AppleScript:", proc.stderr)
    else:
        print("Output:", proc.stdout)
except Exception as e:
    print("Exception occurred:", e)
