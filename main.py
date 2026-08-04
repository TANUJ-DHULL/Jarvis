import sys
from speaker import speak
from listener import listen
from system_ops import open_application, close_application, shutdown_pc, enable_study_mode, disable_study_mode, enable_ultra_study_mode, is_ultra_study_mode_active, close_active_window, minimize_active_window, maximize_active_window
from automation import type_text, press_enter, volume_up, volume_down, mute, volume_full, set_volume, take_screenshot
from web_ops import search_wikipedia, open_youtube, open_google, search_google, open_facebook, open_instagram, open_whatsapp, open_twitter, open_discord, open_telegram, play_on_youtube
from storage import save_entry
from llm_agent import JarvisAgent

# Global flag to track if permission was asked and granted for the current action.
permission_granted_for_current_action = False

def ask_user_permission(action_desc):
    # Speak the permission request in English
    speak(f"Sir, should I {action_desc}?")
    
    # Listen for the user's response
    for attempt in range(3):
        response = listen()
        if response == "none":
            speak("I couldn't hear you, sir. Do I have permission?")
            continue
            
        print(f"DEBUG: Permission response received: {response}")
        # Check for positive/negative responses in English or Hindi/Hinglish translations
        positive_words = ["yes", "yeah", "yup", "ok", "okay", "allow", "go ahead", "haan", "kar do", "yes please", "sure"]
        negative_words = ["no", "nah", "stop", "cancel", "don't", "dont", "nahi", "mat karo", "never"]
        
        if any(word in response for word in positive_words):
            speak("Thank you, sir. Starting the task now.")
            return True
        elif any(word in response for word in negative_words):
            speak("Alright sir, shutting down Jarvis now.")
            return False
            
    # If no response after 3 attempts, treat it as denied/no response and turn off
    speak("No response received, sir. Shutting down for safety.")
    return False

def verified_action(action_name, description_hinglish):
    """
    Decorator/wrapper that executes the action directly without asking for permission.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Wrap action functions for strict permission check
open_application = verified_action("open_application", "open the application")(open_application)
close_application = verified_action("close_application", "close the application")(close_application)
shutdown_pc = verified_action("shutdown_pc", "shut down the PC")(shutdown_pc)
enable_study_mode = verified_action("enable_study_mode", "enable study mode")(enable_study_mode)
disable_study_mode = verified_action("disable_study_mode", "disable study mode")(disable_study_mode)
enable_ultra_study_mode = verified_action("enable_ultra_study_mode", "enable ultra study mode")(enable_ultra_study_mode)
close_active_window = verified_action("close_active_window", "close the active window")(close_active_window)
minimize_active_window = verified_action("minimize_active_window", "minimize the active window")(minimize_active_window)
maximize_active_window = verified_action("maximize_active_window", "maximize the active window")(maximize_active_window)

type_text = verified_action("type_text", "type text")(type_text)
press_enter = verified_action("press_enter", "press enter")(press_enter)
volume_up = verified_action("volume_up", "raise the volume")(volume_up)
volume_down = verified_action("volume_down", "lower the volume")(volume_down)
mute = verified_action("mute", "mute the system")(mute)
set_volume = verified_action("set_volume", "set the volume")(set_volume)

search_wikipedia = verified_action("search_wikipedia", "search Wikipedia")(search_wikipedia)
open_youtube = verified_action("open_youtube", "open YouTube")(open_youtube)
open_google = verified_action("open_google", "open Google")(open_google)
search_google = verified_action("search_google", "search Google")(search_google)
open_facebook = verified_action("open_facebook", "open Facebook")(open_facebook)
open_instagram = verified_action("open_instagram", "open Instagram")(open_instagram)
open_whatsapp = verified_action("open_whatsapp", "open WhatsApp")(open_whatsapp)
open_twitter = verified_action("open_twitter", "open Twitter")(open_twitter)
open_discord = verified_action("open_discord", "open Discord")(open_discord)
open_telegram = verified_action("open_telegram", "open Telegram")(open_telegram)
play_on_youtube = verified_action("play_on_youtube", "play on YouTube")(play_on_youtube)

# Initialize the LLM Agent globally
llm = JarvisAgent()

def process_command(query):
    # Persist each request so we can review command history later.
    save_entry(query, action="received")

    if query == "none":
        save_entry(query, action="no_command")
        return True

    if 'wikipedia' in query:
        results = search_wikipedia(query)
        speak("According to Wikipedia:")
        speak(results)
        save_entry(query, action="wikipedia_search", note=(results[:500] if results else ""))

    elif 'open youtube' in query:
        open_youtube()
        save_entry(query, action="open_youtube")

    elif 'play' in query:
        song = query.replace('play', '').replace('on youtube', '').replace('in youtube', '').strip()
        success = play_on_youtube(song)
        if not success:
            speak(f"Could not play {song} directly on YouTube, sir. Searching for it now.")
            search_google(f"{song} site:youtube.com")
        save_entry(query, action="play_youtube", note=song)

    elif 'video' in query:
        video = query.replace('video', '').replace('on youtube', '').replace('in youtube', '').strip()
        success = play_on_youtube(video)
        if not success:
            speak(f"Could not play {video} directly on YouTube, sir. Searching for it now.")
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
        @verified_action("open_calculator", "open the calculator")
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
            speak(f"Could not find {app_name} on the system. Searching the web.")
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
        speak("Sir, generating content now. Please wait a moment.")
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
            speak(f"Ultra study mode is active. You cannot shut down the PC, sir. {mins} minutes remaining.")
            save_entry(query, action="blocked_by_ultra_study_mode")
            return True

        shutdown_pc()
        save_entry(query, action="shutdown_pc")
        return False

    elif 'stop listening' in query or 'exit' in query or 'quit' in query or 'turn off' in query:
        is_active, remaining = is_ultra_study_mode_active()
        if is_active:
            mins = max(1, remaining // 60)
            speak(f"Ultra study mode is active. You cannot turn me off, sir. {mins} minutes remaining.")
            save_entry(query, action="blocked_by_ultra_study_mode")
            return True

        speak("Goodbye, sir. See you again.")
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
            speak(f"Ultra study mode is active. You cannot disable study mode, sir. {mins} minutes remaining.")
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
            @verified_action("open_url", f"open {args['url']} in the browser")
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
    speak("Jarvis initialized. Welcome back, sir.")
    running = True
    while running:
        query = listen()
        running = process_command(query)
