import subprocess

script = '''
tell application "Google Chrome"
    set t to tab 6 of front window
    set res to execute t javascript "window.location.href"
    return res
end tell
'''
p = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
print("STDOUT:", p.stdout)
print("STDERR:", p.stderr)
