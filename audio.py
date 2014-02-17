import audioop
import pyaudio
import time
from win32api import GetSystemMetrics
import win32api, win32con
import sys
import win32gui

chunk = 1024

p = pyaudio.PyAudio()
REEL_THRESHOLD = 30
SPLASH_THRESHOLD = 500
SILENCE_THRESHOLD = -11

stream = p.open(format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=chunk)

screenWidth = GetSystemMetrics (0)
screenHeight = GetSystemMetrics (1)

rmsMax = 0
t0 = time.clock();

def enumHandler(hwnd, lParam):
    if win32gui.IsWindowVisible(hwnd):
        if 'RIFT' in win32gui.GetWindowText(hwnd):
            win32gui.SetForegroundWindow(hwnd)


def press1():
    win32api.keybd_event(0x31, 0,0,0)
    time.sleep(.05)
    win32api.keybd_event(0x31,0 ,win32con.KEYEVENTF_KEYUP ,0)

def click(x,y):
    win32api.SetCursorPos((x,y))
    print "click: {}, {}".format(x,y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def fishLoop(timeNow, timeout):
    while time.clock() - timeNow < timeout:
        rms = audioop.rms(stream.read(chunk), 2)
        if rms > SILENCE_THRESHOLD: print rms
        if rms > SPLASH_THRESHOLD:
            print "SPLASH THRESHOLD"
            click(screenWidth/2 + 1, screenHeight * 2/3)
            time.sleep(4)
            t1 = time.clock()
            while time.clock() - t1 < 3:
           	rms = audioop.rms(stream.read(chunk), 2)
           	if rms > REEL_THRESHOLD:
           	        if rms > SPLASH_THRESHOLD:
           	            click(screenWidth/2 + 2, screenHeight * 2/3)
           	            return
           	        else:
              		    print "REEL THRESHOLD"
              		    return fishLoop(time.clock(), 10)
            click(screenWidth/2 + 3, screenHeight * 2/3)
            return
    return
#win32gui.EnumWindows(enumHandler, None)
count = 0;
time.sleep(5)
while True:
    count += 1
    print "Casting..."
    press1()
    time.sleep(0.1)
    click(screenWidth/2, screenHeight/2)
    stream.start_stream()
    time.sleep(1)
    print "Fishing..."
    fishLoop(time.clock(), 30)
    stream.stop_stream()
    #click(screenWidth/2, screenHeight * 2/3)
    time.sleep(1)
    print "Finished"
    print count