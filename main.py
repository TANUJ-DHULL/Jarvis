import sys
from speaker import speak
from listener import listen
from system_ops import open_application, close_application, shutdown_pc, enable_study_mode, disable_study_mode, enable_ultra_study_mode, is_ultra_study_mode_active, close_active_window, minimize_active_window, maximize_active_window
from automation import type_text, press_enter, volume_up, volume_down, mute, volume_full, set_volume, take_screenshot
from web_ops import search_wikipedia, open_youtube, open_google, search_google, open_facebook, open_instagram, open_whatsapp, open_twitter, open_discord, open_telegram, play_on_youtube
from storage import save_entry
from llm_agent import EdithAgent

# Global flag to track if permission was asked and granted for the current action.
permission_granted_for_current_action = False

def ask_user_permission(action_desc):
    # Speak the permission request in simple Hinglish
    speak(f"Sir, kya main {action_desc} karu?")
    
    # Listen for the user's response
    for attempt in range(3):
        response = listen()
        if response == "none":
            speak("Mujhe aapki awaz nahi aayi sir. Kya permission hai?")
            continue
            
        print(f"DEBUG: Permission response received: {response}")
        # Check for positive/negative responses in English or Hindi/Hinglish translations
        positive_words = ["yes", "yeah", "yup", "ok", "okay", "allow", "go ahead", "haan", "kar do", "yes please", "sure"]
        negative_words = ["no", "nah", "stop", "cancel", "don't", "dont", "nahi", "mat karo", "never"]
        
        if any(word in response for word in positive_words):
            speak("Dhanyawad sir, main kaam shuru kar raha hoon.")
            return True
        elif any(word in response for word in negative_words):
            speak("Theek hai sir, main abhi band ho raha hoon.")
            return False
            
    # If no response after 3 attempts, treat it as denied/no response and turn off
    speak("Response nahi mila sir, safety ke liye main abhi band ho raha hoon.")
    return False

def verified_action(action_name, description_hinglish):
    """
    Decorator/wrapper that enforces permission checking.
    If the function is called without permission being asked and granted, or if the user denies,
    it automatically turns off (exits).
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            global permission_granted_for_current_action
            
            # If we haven't asked for permission, ask it now.
            if not permission_granted_for_current_action:
                print(f"DEBUG: Checking permission for '{action_name}'...")
                allowed = ask_user_permission(description_hinglish)
                if not allowed:
                    print("Permission denied or not obtained. Shutting down Jarvis.")
                    sys.exit(0) # Automatically turn off
                permission_granted_for_current_action = True
            
            # Reset the flag after execution so the next action must ask again
            permission_granted_for_current_action = False
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Wrap action functions for strict permission check
open_application = verified_action("open_application", "application open karne ki")(open_application)
close_application = verified_action("close_application", "application close karne ki")(close_application)
shutdown_pc = verified_action("shutdown_pc", "PC shut down karne ki")(shutdown_pc)
enable_study_mode = verified_action("enable_study_mode", "study mode active karne ki")(enable_study_mode)
disable_study_mode = verified_action("disable_study_mode", "study mode band karne ki")(disable_study_mode)
enable_ultra_study_mode = verified_action("enable_ultra_study_mode", "ultra study mode active karne ki")(enable_ultra_study_mode)
close_active_window = verified_action("close_active_window", "active window close karne ki")(close_active_window)
minimize_active_window = verified_action("minimize_active_window", "active window minimize karne ki")(minimize_active_window)
maximize_active_window = verified_action("maximize_active_window", "active window maximize karne ki")(maximize_active_window)

type_text = verified_action("type_text", "text type karne ki")(type_text)
press_enter = verified_action("press_enter", "enter key press karne ki")(press_enter)
volume_up = verified_action("volume_up", "volume badhane ki")(volume_up)
volume_down = verified_action("volume_down", "volume kam karne ki")(volume_down)
mute = verified_action("mute", "system mute karne ki")(mute)
set_volume = verified_action("set_volume", "volume set karne ki")(set_volume)

search_wikipedia = verified_action("search_wikipedia", "Wikipedia search karne ki")(search_wikipedia)
open_youtube = verified_action("open_youtube", "YouTube kholne ki")(open_youtube)
open_google = verified_action("open_google", "Google kholne ki")(open_google)
search_google = verified_action("search_google", "Google search karne ki")(search_google)
open_facebook = verified_action("open_facebook", "Facebook kholne ki")(open_facebook)
open_instagram = verified_action("open_instagram", "Instagram kholne ki")(open_instagram)
open_whatsapp = verified_action("open_whatsapp", "WhatsApp kholne ki")(open_whatsapp)
open_twitter = verified_action("open_twitter", "Twitter kholne ki")(open_twitter)
open_discord = verified_action("open_discord", "Discord kholne ki")(open_discord)
open_telegram = verified_action("open_telegram", "Telegram kholne ki")(open_telegram)
play_on_youtube = verified_action("play_on_youtube", "YouTube par play karne ki")(play_on_youtube)

# Initialize the LLM Agent globally
llm = EdithAgent()

def process_command(query):
    # Persist each request so we can review command history later.
    save_entry(query, action="received")

    if query == "none":
        save_entry(query, action="no_command")
        return True

    if 'wikipedia' in query:
        results = search_wikipedia(query)
        speak("Wikipedia ke mutabik:")
        speak(results)
        save_entry(query, action="wikipedia_search", note=(results[:500] if results else ""))

    elif 'open youtube' in query:
        open_youtube()
        save_entry(query, action="open_youtube")

    elif 'play' in query:
        song = query.replace('play', '').replace('on youtube', '').replace('in youtube', '').strip()
        success = play_on_youtube(song)
        if not success:
            speak(f"YouTube par {song} direct play nahi ho paya sir, search kar raha hoon.")
            search_google(f"{song} site:youtube.com")
        save_entry(query, action="play_youtube", note=song)

    elif 'video' in query:
        video = query.replace('video', '').replace('on youtube', '').replace('in youtube', '').strip()
        success = play_on_youtube(video)
        if not success:
            speak(f"YouTube par {video} direct play nahi ho paya sir, search kar raha hoon.")
            search_google(f"{video} site:youtube.com")
        save_entry(query, action="play_youtube", note=video)

    elif 'open google' in query:
        open_google()
        save_entry(query, action="open_google")

    elif 'open facebook' in query:
        open_facebook()
        save_entry(query, action="open_facebook")

    elif 'open instagram' in query:
        open_instagram()
        save_entry(query, action="open_instagram")

    elif 'open whatsapp' in query:
        open_whatsapp()
        save_entry(query, action="open_whatsapp")

    elif 'open twitter' in query:
        open_twitter()
        save_entry(query, action="open_twitter")

    elif 'open discord' in query:
        open_discord()
        save_entry(query, action="open_discord")

    elif 'open telegram' in query:
        open_telegram()
        save_entry(query, action="open_telegram")   

    elif 'open calculator' in query or 'open calc' in query:
        import os
        @verified_action("open_calculator", "calculator open karne ki")
        def open_calc_action():
            os.system("calc")
        open_calc_action()
        save_entry(query, action="open_calculator")
        
    elif 'search' in query:
        search_query = query.replace('search', '').replace('google for', '').replace('google', '').strip()
        if search_query.startswith('for '):
            search_query = search_query[4:]
        search_google(search_query)
        save_entry(query, action="search", note=search_query)

    elif 'open' in query:
        app_name = query.replace('open', '').strip()
        
        success = open_application(app_name)
        if success:
            save_entry(query, action="open_application", note=app_name)
        else:
            speak(f"System me {app_name} nahi mila, web par search kar raha hoon.")
            search_google(f"{app_name}")
            save_entry(query, action="open_application_fallback_web", note=app_name)

    elif 'close this' in query:
        close_active_window()
        save_entry(query, action="close_active_window")

    elif 'minimize this' in query or 'minimise this' in query:
        minimize_active_window()
        save_entry(query, action="minimize_active_window")

    elif 'maximize this' in query or 'maximise this' in query:
        maximize_active_window()
        save_entry(query, action="maximize_active_window")

    elif 'close' in query:
        app_name = query.replace('close', '').strip()
        close_application(app_name)
        save_entry(query, action="close_application", note=app_name)

    elif 'type' in query and 'email' not in query and 'letter' not in query and 'generate' not in query:
        text_to_type = query.replace('type', '').strip()
        text_to_type = text_to_type.replace('at the rate', '@')
        text_to_type = text_to_type.replace('gmail dot com', 'gmail.com')
        
        # Remove all spaces if it looks like an email address
        if '@' in text_to_type and 'gmail' in text_to_type:
            text_to_type = text_to_type.replace(' ', '')
            
        type_text(text_to_type)
        press_enter()
        save_entry(query, action="type_text", note=text_to_type)
        
    elif 'write an email' in query or 'draft an email' in query or 'generate' in query or 'type an email' in query:
        speak("Sir, main code generate kar raha hoon, ek second rukiye.")
        response_data = llm.process_query(query)
        
        if "response" in response_data and response_data.get("response"):
            speak(response_data["response"])
            
        if response_data.get("action_type") == "type_text" and "text" in response_data.get("action_args", {}):
            text_to_write = response_data["action_args"]["text"]
            type_text(text_to_write)
        elif response_data.get("mode") == "chat" and "response" in response_data:
            # Fallback if model puts the email in the response instead of action args
            if len(response_data["response"]) > 100:
                type_text(response_data["response"])
        save_entry(query, action="llm_generate_and_type")
        
    elif 'send this mail' in query or query.strip() == 'enter' or 'press enter' in query:
        press_enter()
        save_entry(query, action="press_enter")

    elif 'volume up' in query:
        volume_up()
        save_entry(query, action="volume_up")

    elif 'volume down' in query:
        volume_down()
        save_entry(query, action="volume_down")
        
    elif 'mute' in query:
        mute()
        save_entry(query, action="mute")

    elif 'shut down' in query or 'shutdown' in query:
        is_active, remaining = is_ultra_study_mode_active()
        if is_active:
            mins = max(1, remaining // 60)
            speak(f"Ultra study mode active hai. Aap abhi shut down nahi kar sakte, sir. {mins} minutes bache hain.")
            save_entry(query, action="blocked_by_ultra_study_mode")
            return True

        shutdown_pc()
        save_entry(query, action="shutdown_pc")
        return False

    elif 'stop listening' in query or 'exit' in query or 'quit' in query or 'turn off' in query:
        is_active, remaining = is_ultra_study_mode_active()
        if is_active:
            mins = max(1, remaining // 60)
            speak(f"Ultra study mode active hai. Aap mujhe abhi band nahi kar sakte sir. {mins} minutes bache hain.")
            save_entry(query, action="blocked_by_ultra_study_mode")
            return True

        speak("Alvida sir. Phir milenge.")
        save_entry(query, action="exit")
        return False

    elif 'volume' in query:
        words = query.split()
        for word in words:
            if word.isdigit():
                vol = int(word)
                if 0 <= vol <= 100:
                    set_volume(vol)
                    save_entry(query, action="set_volume", note=str(vol))
                break

    elif 'ultra study mode' in query:
        enable_ultra_study_mode()
        save_entry(query, action="ultra_study_mode_on")

    elif 'study mode on' in query or 'enable study mode' in query:
        enable_study_mode()
        save_entry(query, action="study_mode_on")

    elif 'study mode off' in query or 'disable study mode' in query:
        is_active, remaining = is_ultra_study_mode_active()
        if is_active:
            mins = max(1, remaining // 60)
            speak(f"Ultra study mode active hai. Aap study mode band nahi kar sakte sir. {mins} minutes bache hain.")
            save_entry(query, action="blocked_by_ultra_study_mode")
            return True

        disable_study_mode()
        save_entry(query, action="study_mode_off")

    else:
        # If it doesn't match any hardcoded commands, ask the LLM!
        response_data = llm.process_query(query)
        action = response_data.get("action_type", "none")
        args = response_data.get("action_args", {})
        
        if response_data.get("response"):
            speak(response_data["response"])
            
        if action == "type_text" and "text" in args:
            type_text(args["text"])
        elif action == "open_app" and "app_name" in args:
            open_application(args["app_name"])
        elif action == "close_app" and "app_name" in args:
            close_application(args["app_name"])
        elif action == "search_google" and "query" in args:
            search_google(args["query"])
        elif action == "open_url" and "url" in args:
            import webbrowser
            @verified_action("open_url", f"browser mein {args['url']} kholne ki")
            def open_url_web(u):
                webbrowser.open_new_tab(u)
            open_url_web(args["url"])
        elif action == "volume_up":
            volume_up()
        elif action == "volume_down":
            volume_down()
        elif action == "mute":
            mute()
            
        save_entry(query, action="llm_fallback")

    return True

if __name__ == "__main__":
    speak("EDITH initialize ho gaya hai. Welcome back sir.")
    running = True
    while running:
        query = listen()
        running = process_command(query)
