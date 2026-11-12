import subprocess, time

targets = [
    # (qid, num_down_arrows, expected_label)
    ("question_64239204", 2, "Java / Spring Boot"),
    ("question_64239205", 1, "Yes (schema)"),
    ("question_65143956", 1, "Yes, multiple times (architecture)"),
    ("question_64239206", 1, "Use daily (ai tools)"),
    ("question_65143957", 1, "Yes, both mentoring (leadership)"),
    ("question_64239208", 1, "Yes (relocate)"),
    ("question_64239209", 2, "Less than 15 days (notice)"),
    ("question_64239211", 2, "No (current offers)")
]

for qid, num_arrows, label in targets:
    # 1. Focus element
    focus_script = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684133)
            execute javascript "var el = document.getElementById('{qid}'); if (el) {{ el.focus(); el.scrollIntoView({{block: 'center'}}); }}"
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', focus_script])
    time.sleep(0.3)

    # 2. Build arrow presses
    arrow_lines = "\n".join(["key code 125\ndelay 0.2" for _ in range(num_arrows)])
    key_script = f'''
    tell application "System Events"
        tell process "Google Chrome"
            {arrow_lines}
            key code 36 -- Return
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', key_script])
    time.sleep(0.4)

    # 3. Verify
    check_script = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684133)
            return (execute javascript "var el = document.getElementById('{qid}'); el ? el.closest('.select__control').innerText.replace(/\\n/g, ' ') : 'NOT_FOUND'")
        end tell
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, _ = p.communicate(check_script)
    print(f"[{qid} - {label}] -> {out.strip()}")
    time.sleep(0.2)

print("\nAll dropdowns completed!")
