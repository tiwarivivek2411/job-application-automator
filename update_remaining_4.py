import subprocess, time

questions_arrows = [
    ("question_64239204", 2), # Java / Spring Boot
    ("question_64239206", 1), # Use daily
    ("question_65143957", 1), # Yes, both mentoring
    ("question_64239209", 2)  # Less than 15 days
]

for qid, num_arrows in questions_arrows:
    # 1. Focus input
    focus_cmd = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684133)
            execute javascript "var el = document.getElementById('{qid}'); if (el) {{ el.focus(); el.scrollIntoView({{block: 'center'}}); }}"
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', focus_cmd])
    time.sleep(0.4)

    # 2. Key events
    arrow_cmds = "\n".join(["key code 125\ndelay 0.25" for _ in range(num_arrows)])
    key_cmd = f'''
    tell application "System Events"
        tell process "Google Chrome"
            {arrow_cmds}
            key code 36 -- Return
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', key_cmd])
    time.sleep(0.4)

    # 3. Check selected value
    check_cmd = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684133)
            return (execute javascript "var el = document.getElementById('{qid}'); el ? el.closest('.select__control').innerText.replace(/\\n/g, ' ') : 'NOT_FOUND'")
        end tell
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, _ = p.communicate(check_cmd)
    print(f"[{qid}] -> {out.strip()}")
    time.sleep(0.2)

print("Dropdowns updated!")
