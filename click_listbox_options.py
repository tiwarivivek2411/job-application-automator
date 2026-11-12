import subprocess, time

js_code = """
(function() {
    var results = [];

    // Helper to click an option inside a specific listbox
    function clickInListbox(listboxId, optionText) {
        var lb = document.getElementById(listboxId);
        if (!lb) return 'NO_LB: ' + listboxId;
        var opts = Array.from(lb.querySelectorAll("[role='option'], .select__option, div"));
        var match = opts.find(o => o.innerText.trim() === optionText || o.innerText.trim().startsWith(optionText));
        if (match) {
            match.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
            match.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
            match.click();
            return 'CLICKED: ' + match.innerText.trim();
        }
        return 'OPT_NOT_FOUND: ' + optionText + ' in ' + lb.innerText.replace(/\\n/g, ' ');
    }

    results.push(clickInListbox('react-select-question_64239206-listbox', 'Use daily'));
    results.push(clickInListbox('react-select-question_65143957-listbox', 'Yes, both mentoring and leading cross-team projects'));
    results.push(clickInListbox('react-select-question_64239209-listbox', 'Less than 15 days'));
    results.push(clickInListbox('react-select-question_64239211-listbox', 'No'));

    return JSON.stringify(results);
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
print("CLICK LISTBOX RESULTS:\n", out)
