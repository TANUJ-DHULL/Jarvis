from speaker import speak
from listener import listen
from system_ops import open_application, close_application, shutdown_pc, enable_study_mode, disable_study_mode, enable_ultra_study_mode, is_ultra_study_mode_active, close_active_window, minimize_active_window, maximize_active_window
from automation import type_text, press_enter, volume_up, volume_down, mute, volume_full, set_volume, take_screenshot
from web_ops import search_wikipedia, open_youtube, open_google, search_google, open_facebook, open_instagram, open_whatsapp, open_twitter, open_discord, open_telegram, play_on_youtube
from storage import save_entry
from llm_agent import EdithAgent

# Initialize the LLM Agent globally
llm = EdithAgent()

def process_command(query):
    # Persist each request so we can review command history later.
    save_entry(query, action="received")

    if query == "none":
        save_entry(query, action="no_command")
        return True

    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        results = search_wikipedia(query)
        speak("According to Wikipedia")
        speak(results)
        save_entry(query, action="wikipedia_search", note=(results[:500] if results else ""))

    elif 'open youtube' in query:
        speak("Opening YouTube")
        open_youtube()
        save_entry(query, action="open_youtube")

    elif 'play' in query:
        song = query.replace('play', '').replace('on youtube', '').replace('in youtube', '').strip()
        speak(f"Playing {song} on YouTube")
        success = play_on_youtube(song)
        if not success:
            speak(f"Could not automatically play {song}, searching instead.")
            search_google(f"{song} site:youtube.com")
        save_entry(query, action="play_youtube", note=song)

    elif 'video' in query:
        video = query.replace('video', '').replace('on youtube', '').replace('in youtube', '').strip()
        speak(f"Playing {video} on YouTube")
        success = play_on_youtube(video)
        if not success:
            speak(f"Could not automatically play {video}, searching instead.")
            search_google(f"{video} site:youtube.com")
        save_entry(query, action="play_youtube", note=video)

    elif 'open google' in query:
        speak("Opening Google")
        open_google()
        save_entry(query, action="open_google")

    elif 'open facebook' in query:
        speak("Opening Facebook")
        open_facebook()
        save_entry(query, action="open_facebook")

    elif 'open instagram' in query:
        speak("Opening Instagram")
        open_instagram()
        save_entry(query, action="open_instagram")

    elif 'open whatsapp' in query:
        speak("Opening WhatsApp")
        open_whatsapp()
        save_entry(query, action="open_whatsapp")

    elif 'open twitter' in query:
        speak("Opening Twitter")
        open_twitter()
        save_entry(query, action="open_twitter")

    elif 'open discord' in query:
        speak("Opening Discord")
        open_discord()
        save_entry(query, action="open_discord")

    elif 'open telegram' in query:
        speak("Opening Telegram")
        open_telegram()
        save_entry(query, action="open_telegram")   

    elif 'open calculator' in query or 'open calc' in query:
        import os
        speak("Opening Calculator")
        os.system("calc")
        save_entry(query, action="open_calculator")
        
    elif 'search' in query:
        search_query = query.replace('search', '').replace('google for', '').replace('google', '').strip()
        if search_query.startswith('for '):
            search_query = search_query[4:]
        speak(f"Searching for {search_query}")
        search_google(search_query)
        save_entry(query, action="search", note=search_query)

    elif 'open' in query:
        app_name = query.replace('open', '').strip()
        
        success = open_application(app_name)
        if success:
            speak(f"Opening {app_name}")
            save_entry(query, action="open_application", note=app_name)
        else:
            speak(f"Searching for {app_name} on the web")
            search_google(f"{app_name}")
            save_entry(query, action="open_application_fallback_web", note=app_name)

    elif 'close this' in query:
        speak("Closing this app")
        close_active_window()
        save_entry(query, action="close_active_window")

    elif 'minimize this' in query or 'minimise this' in query:
        speak("Minimizing this app")
        minimize_active_window()
        save_entry(query, action="minimize_active_window")

    elif 'maximize this' in query or 'maximise this' in query:
        speak("Maximizing this app")
        maximize_active_window()
        save_entry(query, action="maximize_active_window")

    elif 'close' in query:
        app_name = query.replace('close', '').strip()
        speak(f"Closing {app_name}")
        close_application(app_name)
        save_entry(query, action="close_application", note=app_name)

    elif 'create a folder' in query or 'make a folder' in query:
        folder_name = query.replace('create a folder', '').replace('named', '').replace('called', '').replace('make a folder', '').strip()
        if not folder_name:
            folder_name = "New Folder"
        speak(f"Creating a folder named {folder_name} in your local disk.")
        from automation import create_folder_visually
        create_folder_visually(folder_name)
        speak("Folder created successfully.")
        save_entry(query, action="create_folder", note=folder_name)

    elif 'take ss' in query or 'screenshot' in query:
        speak("Taking a screenshot sir.")
        filename = take_screenshot()
        speak("Screenshot saved.")
        save_entry(query, action="take_screenshot", note=filename)

    elif 'type' in query and 'email' not in query and 'letter' not in query and 'generate' not in query:
        text_to_type = query.replace('type', '').strip()
        text_to_type = text_to_type.replace('at the rate', '@')
        text_to_type = text_to_type.replace('gmail dot com', 'gmail.com')
        
        # Remove all spaces if it looks like an email address
        if '@' in text_to_type and 'gmail' in text_to_type:
            text_to_type = text_to_type.replace(' ', '')
            
        speak(f"Typing: {text_to_type}")
        type_text(text_to_type)
        press_enter()
        save_entry(query, action="type_text", note=text_to_type)

    elif 'make a website' in query or 'html website' in query or 'html code' in query:
        speak("Generating the website code for you sir. Please wait a moment.")
        custom_prompt = f"The user requested to create a website with the following query: '{query}'. Provide ONLY the raw HTML/CSS code for this website. Create a beautiful and complete 1-page design inside a single HTML file. Do not include markdown formatting like ```html. Output raw code that can be typed directly into an editor."
        response_data = llm.process_query(custom_prompt)
        
        text_to_write = ""
        if response_data.get("action_type") == "type_text" and "text" in response_data.get("action_args", {}):
            text_to_write = response_data["action_args"]["text"]
        elif response_data.get("response"):
            text_to_write = response_data["response"]

        if text_to_write:
            # Clean up the output in case the model added markdown blocks
            if "```html" in text_to_write:
                text_to_write = text_to_write.split("```html")[1].split("```")[0]
            elif "```" in text_to_write:
                text_to_write = text_to_write.split("```")[1]
                
            text_to_write = text_to_write.strip()
            speak("Coding the website now.")
            type_text(text_to_write)
        else:
            speak("I could not generate the website code.")
            
        save_entry(query, action="generate_website")
        
    elif 'write an email' in query or 'draft an email' in query or 'generate' in query or 'type an email' in query:
        speak("Generating that for you sir. Please wait a second.")
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
        speak("Pressing enter")
        press_enter()
        save_entry(query, action="press_enter")

    elif 'volume up' in query:
        volume_up()
        speak("Volume increased")
        save_entry(query, action="volume_up")

    elif 'volume down' in query:
        volume_down()
        speak("Volume decreased")
        save_entry(query, action="volume_down")
        
    elif 'mute' in query:
        mute()
        save_entry(query, action="mute")

    elif 'shut down' in query or 'shutdown' in query:
        is_active, remaining = is_ultra_study_mode_active()
        if is_active:
            mins = max(1, remaining // 60)
            speak(f"Ultra study mode is active. You cannot shut down right now. {mins} minutes remaining.")
            save_entry(query, action="blocked_by_ultra_study_mode")
            return True

        speak("Shutting down the PC in 5 seconds. Goodbye sir.")
        shutdown_pc()
        save_entry(query, action="shutdown_pc")
        return False

    elif 'stop listening' in query or 'exit' in query or 'quit' in query or 'turn off' in query:
        is_active, remaining = is_ultra_study_mode_active()
        if is_active:
            mins = max(1, remaining // 60)
            speak(f"Ultra study mode is active. You cannot turn me off right now. {mins} minutes remaining.")
            save_entry(query, action="blocked_by_ultra_study_mode")
            return True

        speak("Goodbye sir.")
        save_entry(query, action="exit")
        return False

    elif 'volume' in query:
        words = query.split()
        for word in words:
            if word.isdigit():
                vol = int(word)
                if 0 <= vol <= 100:
                    set_volume(vol)
                    speak(f"Volume set to {vol}")
                    save_entry(query, action="set_volume", note=str(vol))
                break

    elif 'ultra study mode' in query:
        enable_ultra_study_mode()
        speak("Ultra study mode activated for one hour. All distractions and exits are blocked.")
        save_entry(query, action="ultra_study_mode_on")

    elif 'study mode on' in query or 'enable study mode' in query:
        enable_study_mode()
        speak("Study mode activated. Social media apps will be blocked.")
        save_entry(query, action="study_mode_on")

    elif 'study mode off' in query or 'disable study mode' in query:
        is_active, remaining = is_ultra_study_mode_active()
        if is_active:
            mins = max(1, remaining // 60)
            speak(f"Ultra study mode is active. You cannot disable it right now. {mins} minutes remaining.")
            save_entry(query, action="blocked_by_ultra_study_mode")
            return True

        disable_study_mode()
        speak("Study mode deactivated.")
        save_entry(query, action="study_mode_off")

    else:
        # If it doesn't match any hardcoded commands, ask the LLM!
        response_data = llm.process_query(query)
        action = response_data.get("action_type", "none")
        
        if response_data.get("response"):
            speak(response_data["response"])
            
        if action == "type_text" and "text" in response_data.get("action_args", {}):
            type_text(response_data["action_args"]["text"])
            
        save_entry(query, action="llm_fallback")

    return True

if __name__ == "__main__":
    speak("EDITH initializing. Welcome back sir.")
    running = True
    while running:
        query = listen()
        running = process_command(query)
