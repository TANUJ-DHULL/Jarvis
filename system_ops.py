import os
import threading
import time
import contextlib
import io
import ctypes
import pyautogui
from AppOpener import open as appopen, close as appclose

study_mode_active = False
ultra_study_mode_active = False
ultra_study_mode_end_time = 0

def enable_study_mode():
    global study_mode_active
    study_mode_active = True

def enable_ultra_study_mode():
    global study_mode_active, ultra_study_mode_active, ultra_study_mode_end_time
    study_mode_active = True
    ultra_study_mode_active = True
    ultra_study_mode_end_time = time.time() + 3600

def disable_study_mode():
    global study_mode_active, ultra_study_mode_active
    study_mode_active = False
    ultra_study_mode_active = False

def is_ultra_study_mode_active():
    global ultra_study_mode_active, ultra_study_mode_end_time
    if ultra_study_mode_active:
        if time.time() >= ultra_study_mode_end_time:
            ultra_study_mode_active = False
            return False, 0
        else:
            remaining = int(ultra_study_mode_end_time - time.time())
            return True, remaining
    return False, 0

def get_active_window_title():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value if buf.value else ""

def block_social_media_worker():
    import re
    # Expanded blacklist for social media, games, and entertainment sites
    distraction_keywords = [
        "instagram", "facebook", "whatsapp", "twitter", "discord", "telegram",
        "netflix", "prime video", "hotstar", "amazon prime", "disney", "hulu", "movies",
        "steam", "epic games", "valorant", "gta", "minecraft", "roblox", "twitch",
        "reddit", "tiktok", "snapchat", "spotify", "anime", "crunchyroll"
    ]
    # Executables for communication and games
    executables_to_kill = [
        "WhatsApp.exe", "Discord.exe", "Telegram.exe",
        "steam.exe", "EpicGamesLauncher.exe", "VALORANT-Win64-Shipping.exe", 
        "Spotify.exe"
    ]
    
    unapproved_yt_tabs = {}
    
    while True:
        if study_mode_active:
            # 1. Aggressively kill known executables
            for exe in executables_to_kill:
                os.system(f'taskkill /F /IM {exe} >nul 2>&1')
                
            # 2. Check active window for distracting websites (browsers/apps)
            try:
                active_title = get_active_window_title().lower()
                
                # Check for YouTube specifically during Ultra Study Mode
                if ultra_study_mode_active and 'youtube' in active_title:
                    yt_allowed_keywords = [
                        'study', 'business', 'shark tank', 'founder', 'code', 'learn', 
                        'course', 'tutorial', 'education', 'lecture', 'podcast', 'finance', 
                        'economy', 'tech', 'programming', 'developer', 'startup',
                        'class', 'chapter', 'syllabus', 'physics', 'math', 'chemistry', 
                        'biology', 'engineering', 'medical', 'upsc', 'jee', 'neet', 
                        'react', 'python', 'java', 'javascript', 'html', 'css', 'ai', 
                        'machine learning', 'data', 'algorithm', 'entrepreneur', 
                        'marketing', 'sales', 'growth', 'money', 'investing', 'stock', 
                        'trading', 'exam', 'revision', 'guide', 'how to'
                    ]
                    # Remove browser suffix to simplify
                    clean_title = active_title.split(' - google chrome')[0].split(' - brave')[0].split(' - mozilla')[0].split(' - microsoft edge')[0]
                    clean_title = clean_title.strip()
                    
                    # Check if it's the homepage with or without notifications e.g. "(2) youtube" or "youtube"
                    is_homepage = re.match(r'^(\(\d+\)\s*)?youtube$', clean_title) or clean_title == "youtube music"
                    
                    if not is_homepage:
                        # It's a video or search. Does it have educational keywords?
                        is_yt_educational = any(k in clean_title for k in yt_allowed_keywords)
                        if not is_yt_educational:
                            # Not educational! Give a 5-second grace period for them to search or load title
                            if active_title not in unapproved_yt_tabs:
                                unapproved_yt_tabs[active_title] = time.time()
                            elif time.time() - unapproved_yt_tabs[active_title] > 5:
                                pyautogui.hotkey('ctrl', 'w')
                                time.sleep(0.5)
                                if active_title in unapproved_yt_tabs:
                                    del unapproved_yt_tabs[active_title]
                            continue # Skip rest of checks
                        else:
                            # If it's educational, remove from unapproved list if it was there
                            if active_title in unapproved_yt_tabs:
                                del unapproved_yt_tabs[active_title]
                            
                # General Distraction Checking
                # Check if it's explicitly allowed to overrule broad matching
                allowed_keywords = ["chatgpt", "gemini", "claude", "study", "code", "learn", "course"]
                is_allowed = any(allowed in active_title for allowed in allowed_keywords)
                
                if not is_allowed:
                    for keyword in distraction_keywords:
                        if keyword in active_title:
                            # Attempt to close the tab
                            pyautogui.hotkey('ctrl', 'w')
                            time.sleep(0.5)
                            
                            # If still there (maybe a standalone app), force close window
                            current_title = get_active_window_title().lower()
                            if current_title == active_title and keyword in current_title:
                                pyautogui.hotkey('alt', 'f4')
                            break
            except Exception:
                pass
                
        time.sleep(2)

# Start background thread
threading.Thread(target=block_social_media_worker, daemon=True).start()

def open_application(app_name):
    try:
        appopen(app_name, match_closest=False, throw_error=True)
        return True
    except Exception as e:
        print(f"Could not open {app_name}: {e}")
        return False

def close_application(app_name):
    try:
        appclose(app_name, match_closest=False, throw_error=True)
        return True
    except Exception as e:
        print(f"Could not close {app_name}: {e}")
        return False

def shutdown_pc():
    try:
        os.system("shutdown /s /t 5")
        return True
    except Exception as e:
        print(f"Could not shut down the PC: {e}")
        return False

def close_active_window():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    if hwnd:
        ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0) # WM_CLOSE

def minimize_active_window():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 6) # SW_MINIMIZE

def maximize_active_window():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
