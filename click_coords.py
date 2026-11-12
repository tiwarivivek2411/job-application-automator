import sys
import time
from Quartz.CoreGraphics import (
    CGEventCreateMouseEvent,
    CGEventPost,
    kCGEventMouseMoved,
    kCGEventLeftMouseDown,
    kCGEventLeftMouseUp,
    kCGMouseButtonLeft,
    kCGHIDEventTap
)

def click(x, y):
    point = (x, y)
    move = CGEventCreateMouseEvent(None, kCGEventMouseMoved, point, kCGMouseButtonLeft)
    down = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, point, kCGMouseButtonLeft)
    up = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, point, kCGMouseButtonLeft)
    
    CGEventPost(kCGHIDEventTap, move)
    time.sleep(0.1)
    CGEventPost(kCGHIDEventTap, down)
    time.sleep(0.1)
    CGEventPost(kCGHIDEventTap, up)
    print(f"Clicked at ({x}, {y})")

if __name__ == "__main__":
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    click(x, y)
