import subprocess, time

# 1. Open question_64239204 listbox
open_js = """
(function() {
    var inp = document.getElementById('question_64239204');
    if (!inp) return 'NO_INP';
    inp.focus();
    var c = inp.closest('.select__control') || inp.parentElement;
    if (c) {
        c.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        c.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
        c.click();
    }
    return 'OPENED_STACK';
})()
"""
cleaned_open = ' '.join([l.strip() for l in open_js.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
ascript_open = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{cleaned_open}")
    end tell
end tell
'''
subprocess.run(['osascript', '-e', ascript_open])
time.sleep(0.4)

# 2. Click Java / Spring Boot or Node.js in react-select-question_64239204-listbox
click_js = """
(function() {
    var lb = document.getElementById('react-select-question_64239204-listbox');
    if (!lb) {
        var allLbs = document.querySelectorAll("[role='listbox'], [id*='listbox']");
        var found = Array.from(allLbs).map(l => l.id);
        return 'LB_NOT_FOUND, available: ' + JSON.stringify(found);
    }
    var opts = Array.from(lb.querySelectorAll("[role='option'], .select__option, div"));
    var match = opts.find(o => o.innerText.includes('Java') || o.innerText.includes('Node.js'));
    if (match) {
        match.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        match.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
        match.click();
        return 'CLICKED_STACK: ' + match.innerText.trim();
    }
    return 'STACK_OPT_NOT_FOUND in: ' + lb.innerText.replace(/\\n/g, ' ');
})()
"""
cleaned_click = ' '.join([l.strip() for l in click_js.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
ascript_click = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{cleaned_click}")
    end tell
end tell
'''
p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript_click)
print("SELECT STACK RESULT:", out.strip())
