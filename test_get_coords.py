import subprocess
import json

def get_chrome_bounds():
    ascript = '''
    tell application "Google Chrome"
        set b to bounds of window 1
        return "" & (item 1 of b) & "," & (item 2 of b) & "," & (item 3 of b) & "," & (item 4 of b)
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = p.communicate(input=ascript.encode('utf-8'))
    parts = [int(x) for x in out.decode('utf-8').strip().split(',')]
    return parts

from inspect_linkedin_view import run_js
btn_rect_js = """
(() => {
    const btn = Array.from(document.querySelectorAll('button'))
        .find(b => b.offsetWidth > 0 && b.innerText && b.innerText.toLowerCase().includes('easy apply'));
    if (!btn) return 'NO_BTN';
    const r = btn.getBoundingClientRect();
    return JSON.stringify({
        left: r.left,
        top: r.top,
        width: r.width,
        height: r.height,
        winInnerWidth: window.innerWidth,
        winInnerHeight: window.innerHeight,
        winOuterWidth: window.outerWidth,
        winOuterHeight: window.outerHeight
    });
})()
"""

bounds = get_chrome_bounds()
rect_str, _ = run_js(btn_rect_js)
print("CHROME BOUNDS:", bounds)
print("BTN RECT:", rect_str)
