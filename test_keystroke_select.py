import subprocess, time

# Focus input
focus_ascript = '''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        execute javascript "document.getElementById('question_64239203').focus();"
    end tell
end tell
'''
subprocess.run(['osascript', '-e', focus_ascript])
time.sleep(0.5)

# Press Down Arrow then Return via System Events
key_ascript = '''
tell application "System Events"
    tell process "Google Chrome"
        key code 125 -- Down arrow
        delay 0.3
        key code 125 -- Down arrow (second item: 3-5 years)
        delay 0.3
        key code 125 -- Down arrow (third item: 3-5 years)
        delay 0.3
        key code 36  -- Return
    end tell
end tell
'''
subprocess.run(['osascript', '-e', key_ascript])
time.sleep(0.5)

# Inspect selected value
check_ascript = '''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "document.getElementById('question_64239203').closest('.select__control').innerText")
    end tell
end tell
'''
p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(check_ascript)
print("SELECTED VALUE VIA ARROWS:", out.strip())
