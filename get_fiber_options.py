import subprocess, json

js_code = """
(function() {
    var results = {};
    document.querySelectorAll(".select__input").forEach(function(inp) {
        var id = inp.id;
        // React select stores options on parent fiber or select container
        var container = inp.closest(".select__container") || inp.closest("[class*='container']") || inp.parentElement;
        var key = Object.keys(inp).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactProps'));
        var options = [];
        if (key && inp[key]) {
            var fiber = inp[key];
            var curr = fiber;
            while (curr && options.length === 0) {
                if (curr.memoizedProps && curr.memoizedProps.options) {
                    options = curr.memoizedProps.options.map(o => o.label || o.value || o);
                } else if (curr.pendingProps && curr.pendingProps.options) {
                    options = curr.pendingProps.options.map(o => o.label || o.value || o);
                }
                curr = curr.return;
            }
        }
        results[id] = options;
    });
    return JSON.stringify(results);
})()
"""

cleaned_lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
escaped = ' '.join(cleaned_lines).replace('\\', '\\\\').replace('"', '\\"')

ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{escaped}")
    end tell
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("OPTIONS VIA REACT FIBER:", out)
