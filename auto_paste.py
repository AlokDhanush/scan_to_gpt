import pyautogui
import pyperclip
import webbrowser
import time

# Read extracted text
with open("last_extracted.txt", "r", encoding="utf-8") as f:
    text = f.read()

pyperclip.copy(text)

# Open ChatGPT
webbrowser.open("https://chat.openai.com/")
time.sleep(10)  # Wait for page load

pyautogui.hotkey("ctrl", "v")
