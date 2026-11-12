import subprocess, time

# Fix question_65143956 (architecture) to 'Yes, multiple times'
js1 = """
(function() {
    var allEls = Array.from(document.querySelectorAll('.select__option, [id*="-option-"]'));
    var match = allEls.find(e => e.innerText.trim() === 'Yes, multiple times');
    if (match) {
        match.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        match.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
        match.click();
        return 'SET_YES_MULTIPLE';
    }
    return 'NOT_FOUND_YES_MULTIPLE';
})()
"""

# Fix question_64239208 (relocate bangalore) to 'Yes'
# Focus question_64239208
focus_script = '''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        execute javascript "document.getElementById('question_64239208').focus();"
    end tell
end tell
'''
subprocess.run(['osascript', '-e', focus_script])
time.sleep(0.3)

key_script = '''
tell application "System Events"
    tell process "Google Chrome"
        key code 125 -- Down arrow
        delay 0.2
        key code 36  -- Return
    end tell
end tell
'''
subprocess.run(['osascript', '-e', key_script])
time.sleep(0.4)

# Also fix question_65143956
focus_script2 = '''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        execute javascript "document.getElementById('question_65143956').focus();"
    end tell
end tell
'''
subprocess.run(['osascript', '-e', focus_script2])
time.sleep(0.3)

key_script2 = '''
tell application "System Events"
    tell process "Google Chrome"
        key code 125 -- Down arrow (Yes, multiple times)
        delay 0.2
        key code 36  -- Return
    end tell
end tell
'''
subprocess.run(['osascript', '-e', key_script2])
time.sleep(0.4)

print("Done fixing architecture and relocate fields!")
