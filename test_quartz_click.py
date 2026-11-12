import subprocess
import time
import Quartz

def click_screen(x, y):
    # Move mouse
    move_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, move_event)
    time.sleep(0.1)

    # Mouse down
    down_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, down_event)
    time.sleep(0.1)

    # Mouse up
    up_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, up_event)

# Activate Chrome and LinkedIn tab
ascript = '''
tell application "Google Chrome"
    activate
    repeat with w in windows
        set tabIdx to 0
        repeat with t in tabs of w
            set tabIdx to tabIdx + 1
            if (URL of t as string) contains "linkedin.com" then
                set active tab index of w to tabIdx
                set index of w to 1
                return "ACTIVATED"
            end if
        end repeat
    end repeat
    return "NOT_FOUND"
end tell
'''
p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.communicate(input=ascript.encode('utf-8'))

time.sleep(1.0)
print("Clicking at (825, 665)...")
click_screen(825, 665)
time.sleep(2.5)

from inspect_linkedin_view import run_js
check_js = """
(() => {
    const modal = document.querySelector('[role="dialog"], .jobs-easy-apply-modal, .artdeco-modal');
    return modal ? 'MODAL_OPEN: ' + modal.innerText.replace(/\\n/g, ' ').slice(0, 150) : 'NO_MODAL';
})()
"""
out, _ = run_js(check_js)
print(out)
