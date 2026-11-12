import subprocess
import json
import time
import Quartz
import os

PROFILE_PATH = '/Users/nileshtiwari/.gemini/antigravity/scratch/candidate_profile.json'
with open(PROFILE_PATH, 'r') as f:
    PROFILE = json.load(f)

QUESTIONS_LOG_PATH = '/Users/nileshtiwari/.gemini/antigravity/scratch/linkedin_collected_questions.json'
if os.path.exists(QUESTIONS_LOG_PATH):
    with open(QUESTIONS_LOG_PATH, 'r') as f:
        COLLECTED_QUESTIONS = json.load(f)
else:
    COLLECTED_QUESTIONS = {}

APPLIED_JOBS_PATH = '/Users/nileshtiwari/.gemini/antigravity/scratch/linkedin_applied_jobs.json'
if os.path.exists(APPLIED_JOBS_PATH):
    with open(APPLIED_JOBS_PATH, 'r') as f:
        APPLIED_JOBS = json.load(f)
else:
    APPLIED_JOBS = []

def run_js_in_tab(tab_idx, js_code):
    lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
    one_liner = ' '.join(lines).replace('\\', '\\\\').replace('"', '\\"')
    ascript = f'''
    tell application "Google Chrome"
        return (execute tab {tab_idx} of window 1 javascript "{one_liner}")
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=ascript.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def click_screen(x, y):
    move_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, move_event)
    time.sleep(0.1)
    down_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, down_event)
    time.sleep(0.1)
    up_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, up_event)

def activate_tab(tab_idx):
    ascript = f'''
    tell application "Google Chrome"
        activate
        set index of window 1 to 1
        set active tab index of window 1 to {tab_idx}
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate(input=ascript.encode('utf-8'))
    time.sleep(0.5)

print("Helper functions initialized.")
