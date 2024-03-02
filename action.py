import os 
if os.name == 'nt': import mouse
else: import macmouse

def click():
    try:
        mouse.click()
    except: 
        macmouse.click()

def move(x, y):
    try: 
        mouse.move(x, y)
    except: 
        macmouse.move(x, y)

def press(button):
    try:
        mouse.press(button=button)
    except: 
        macmouse.press(button=button)

def release(button):
    try:
        mouse.release(button=button)
    except: 
        macmouse.release(button=button)

