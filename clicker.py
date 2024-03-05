import webbrowser
from pynput.keyboard import Key, Controller
import mouse
import pyautogui
import time

def openWeb(url):
    webbrowser.open(url, new=2)
    time.sleep(2)
    pyautogui.click(1060,880)
    pyautogui.typewrite("Lyle241")
    pyautogui.click(1060,980)