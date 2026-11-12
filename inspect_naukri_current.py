import subprocess

def run_js(js_code, filter_url="naukri.com"):
    cleaned_lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
    escaped = ' '.join(cleaned_lines).replace('\\', '\\\\').replace('"', '\\"')
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "{filter_url}" then
                    return (execute t javascript "{escaped}")
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=ascript.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

js = """
(() => {
    return JSON.stringify({
        url: window.location.href,
        title: document.title,
        textSnippet: document.body.innerText.slice(0, 3000),
        modalsOrDrawers: Array.from(document.querySelectorAll('[role="dialog"], .drawer, .applyModal, .chatbot, .form-container, .layerWrap')).map(d => ({
            cls: d.className,
            text: d.innerText.replace(/\\n/g, '  ')
        })),
        inputs: Array.from(document.querySelectorAll('input, select, textarea')).filter(i => i.offsetWidth > 0 || i.value).map(i => ({
            tag: i.tagName,
            type: i.type,
            name: i.name,
            placeholder: i.placeholder,
            value: i.value,
            checked: i.checked,
            label: i.closest('label, div, p')?.innerText?.replace(/\\n/g, ' ')?.slice(0, 100) || ''
        }))
    });
})()
"""

out, err = run_js(js)
print(out)
