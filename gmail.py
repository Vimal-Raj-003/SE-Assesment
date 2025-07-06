import pyautogui
import time
import pyperclip
import subprocess

# ============ CONFIGURATION ============ #
EMAIL_TO = "vims20.vs@gmail.com"
EMAIL_SUBJECT = "PyAutoGUI Automation"
EMAIL_BODY = """I am very happy to create the automation through PyAutoGUI.
Thank you so much for socially good."""
GMAIL_URL = "https://mail.google.com"

# ============ STEP 1: OPEN CHROME ============ #
print("[INFO] Launching Chrome...")
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
subprocess.Popen(chrome_path)
time.sleep(3)

pyautogui.click(1031,648)
time.sleep(3)

pyautogui.click(310,391)
time.sleep(2)

# ============ STEP 2: OPEN GMAIL ============ #
print("[INFO] Opening Gmail...")
pyautogui.hotkey("ctrl", "l")  # focus address bar
time.sleep(1)
pyperclip.copy(GMAIL_URL)
pyautogui.hotkey("ctrl", "v")
pyautogui.press("enter")
time.sleep(10)  # wait for Gmail to load (adjust if net is slow)

# ============ STEP 3: CLICK "COMPOSE" ============ #
print("[INFO] Clicking Compose...")
# Replace with your screen coordinates (use pyautogui.position())
pyautogui.moveTo(55, 201, duration=1)  # Approx location of Compose button
pyautogui.click()
time.sleep(5)

pyautogui.click(564,968)
time.sleep(2)
# ============ STEP 4: ENTER EMAIL DETAILS ============ #
print("[INFO] Filling in email fields...")

# TO field
pyperclip.copy(EMAIL_TO)
pyautogui.hotkey("ctrl", "v")
pyautogui.press("tab")  # move to Subject
time.sleep(1)

# SUBJECT field
pyperclip.copy(EMAIL_SUBJECT)
pyautogui.hotkey("ctrl", "v")
pyautogui.press("tab")  # move to body
time.sleep(1)

# BODY field
pyperclip.copy(EMAIL_BODY)
pyautogui.hotkey("ctrl", "v")
time.sleep(2)

# ============ STEP 5: CLICK SEND ============ #
print("[INFO] Sending email...")
pyautogui.hotkey("ctrl", "enter")  # Gmail shortcut to send
time.sleep(2)

print("[SUCCESS] Email sent successfully via PyAutoGUI!")
