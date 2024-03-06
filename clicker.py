import webbrowser
from pynput.keyboard import Key, Controller
import mouse
import pyautogui
import time
import subprocess

def openWeb(url):
    #webbrowser.open("https://www.tutorialspoint.com/whiteboard.htm", new=2)
    #webbrowser.open(url, new=2)
    subprocess.Popen(f"start chrome /new-tab {url}", shell = True)
    """time.sleep(1)
    pyautogui.click(1060,880)
    pyautogui.typewrite("Lyle241")
    pyautogui.click(1060,980)"""
    
if __name__ == "__main__":
    openWeb("https://www.tutorialspoint.com/whiteboard.htm")