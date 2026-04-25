import pyautogui
import time

def type_text(text):
    pyautogui.typewrite(text, interval=0.05)

def press_enter():
    pyautogui.press('enter')

def volume_up(presses=5):
    for idx in range(presses):
        pyautogui.press('volumeup')
        time.sleep(0.1)

def volume_down(presses=5):
    for idx in range(presses):
        pyautogui.press('volumedown')
        time.sleep(0.1)

def mute():
    pyautogui.press('volumemute')

def volume_full():
    for _ in range(50):
        pyautogui.press('volumeup')

def set_volume(percentage):
    percentage = max(0, min(100, int(percentage)))
    # lower to 0
    for _ in range(50):
        pyautogui.press('volumedown')
    
    # 1 press = 2% increment
    presses = percentage // 2
    for _ in range(presses):
        pyautogui.press('volumeup')

def take_screenshot():
    import os
    from datetime import datetime
    
    # Save the screenshot in the PC's default Pictures/Screenshots gallery
    pictures_dir = os.path.join(os.path.expanduser('~'), 'Pictures', 'Screenshots')
    if not os.path.exists(pictures_dir):
        os.makedirs(pictures_dir)
        
    filename = os.path.join(pictures_dir, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    pyautogui.screenshot(filename)
    return filename

def create_folder_visually(folder_name):
    import os
    import time
    
    # Open File Manager to Local Disk C (or Documents if C is restricted, but the user requested local disk)
    os.system("explorer C:\\")
    time.sleep(1.5)  # Wait for File Explorer to open
    
    # Press Ctrl+Shift+N to create a new folder
    pyautogui.hotkey('ctrl', 'shift', 'n')
    time.sleep(0.8)  # Wait for the folder to be created and name highlighted
    
    # Type the requested folder name and press Enter
    pyautogui.typewrite(folder_name, interval=0.08)
    pyautogui.press('enter')
