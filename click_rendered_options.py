import subprocess, json, time

js_code = """
(function() {
    var targets = [
        "Java / Spring Boot",
        "Use daily",
        "Yes, both mentoring and leading cross-team projects",
        "Yes",
        "Less than 15 days",
        "No"
    ];

    var allEls = Array.from(document.querySelectorAll("div, li, span, p"));
    var clicked = [];

    targets.forEach(function(t) {
        var match = allEls.find(function(el) {
            return el.children.length === 0 && el.innerText.trim() === t && (el.className.includes('option') || el.id.includes('option') || el.closest('[class*=\"menu\"]') || el.closest('[class*=\"select\"]'));
        });
        if (match) {
            match.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
            match.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
            match.click();
            clicked.push(t);
        }
    });

    return JSON.stringify(clicked);
})()
"""

cleaned = ' '.join([l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')

ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{cleaned}")
    end tell
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("CLICKED OPTIONS VIA DOM:", out)
if err: print("ERR:", err)
