import pyautogui

def shortcut(keys):
    pyautogui.hotkey(*keys)

def action(name,arg1 = None,arg2 = None):
    if name == "move":
        pyautogui.moveTo(arg1,arg2)
    elif name == "click":
        pyautogui.click()
    elif name == "left":
        shortcut(["left"])
    elif name == "right":
        shortcut(["right"])