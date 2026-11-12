import subprocess, json, base64, time

js_code = """
(function() {
    var res = {};

    function setReactValue(el, val) {
        if (!el) return false;
        var proto = el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
        var setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
    }

    res['name'] = setReactValue(document.getElementById('_systemfield_name'), 'Nilesh Tiwari');
    res['email'] = setReactValue(document.getElementById('_systemfield_email'), 'tiwarivivek2411@gmail.com');
    res['linkedin'] = setReactValue(document.getElementById('5fe63700-5ae8-4046-a66d-3ca8ced897ef'), 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    res['github'] = setReactValue(document.getElementById('871e5635-75cc-4305-9df5-8cb59b672b69'), 'https://github.com/nileshtiwari');
    res['source'] = setReactValue(document.getElementById('2d492ae5-0a76-415e-af7f-0f95a9e28b8c'), 'Open-source community and GitHub trending repositories');
    res['location'] = setReactValue(document.getElementById('3a05a4a2-7746-4031-9183-ec0ca0b0ffec'), 'Bengaluru, India');
    res['relocate'] = setReactValue(document.getElementById('6bcdd0d0-d069-424e-b418-ab40f4ba3e75'), 'Yes, open to relocation');
    res['join_date'] = setReactValue(document.getElementById('15deb6dc-a365-424a-8f0d-3a5ef7fc5678'), 'Immediate / 15 Days');
    res['last_day'] = setReactValue(document.getElementById('416d1429-9fcc-43e8-ae3e-513939e96b75'), 'Feb 2026');
    res['current_ctc'] = setReactValue(document.getElementById('5e8d7ef9-93df-4f46-bd90-d7e13355388f'), '35 LPA');
    res['total_exp'] = setReactValue(document.getElementById('6fe11042-2ee7-40d8-97d6-203b8627c77c'), '4.5 Years');

    // Click Yes for AI coding agents
    var aiQ = Array.from(document.querySelectorAll('fieldset, div')).find(c => c.innerText && c.innerText.includes('AI coding'));
    if (aiQ) {
        var yesBtn = Array.from(aiQ.querySelectorAll('button')).find(b => b.innerText.trim() === 'Yes');
        if (yesBtn) {
            yesBtn.click();
            res['ai_coding'] = 'CLICKED_YES';
        }
    }

    return JSON.stringify(res);
})()
"""

ascript_payload = base64.b64encode(js_code.encode('utf-8')).decode('utf-8')
ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "eval(atob('{ascript_payload}'))")
    end tell
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("FILL PLANE PYTHON OUT:\n", out.strip())

time.sleep(2)

# Now submit
submit_js = """
(function() {
    var btn = Array.from(document.querySelectorAll("button")).find(b => b.innerText && b.innerText.includes("Submit Application"));
    if (btn && !btn.disabled) {
        btn.click();
        return "CLICKED_SUBMIT";
    }
    return "CANNOT_SUBMIT: " + (btn ? "disabled" : "not found");
})()
"""
escaped_sub = submit_js.replace('\n', ' ').replace('"', '\\"')
ascript_sub = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{escaped_sub}")
    end tell
end tell
'''
p2 = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out2, err2 = p2.communicate(ascript_sub)
print("SUBMIT ACTION:", out2.strip())
