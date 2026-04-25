import speech_recognition as sr
import subprocess
import os
import sys

# Change to the directory of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def listen_for_wake_word():
    r = sr.Recognizer()
    
    # Optional: adjust these to make background listening less resource-heavy
    r.dynamic_energy_threshold = True
    r.energy_threshold = 400
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("EDITH Wake Engine is running silently in the background...")
        print("Say 'edith on' or 'wake up edith' to start the main systems.")
        
        wake_detected = False
        while True:
            try:
                # Listen in short chunks
                audio = r.listen(source, timeout=1, phrase_time_limit=3)
                query = r.recognize_google(audio, language="en-IN").lower()
                
                print(f"Heard: {query}")
                
                # Check for just 'edith' or 'edith on'
                if "edith on" in query or "wake up" in query or "edith wake" in query or query.strip() == "edith":
                    print("Wake word detected! Launching EDITH main systems...")
                    wake_detected = True
                    break  # Break out of the 'with' block to release microphone
                    
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                pass
                
    # Outside the 'with' block, microphone is released.
    if wake_detected:
        try:
            from speaker import speak
            speak("Waking up sir.")
        except:
            pass
            
        python_exe = sys.executable
        main_script = os.path.join(os.getcwd(), "main.py")
        
        print(f"Running: {python_exe} {main_script}")
        # Launch main process and wait for it to finish
        process = subprocess.Popen([python_exe, main_script])
        process.wait()
        
        print("EDITH main systems shut down. Returning to sleep mode...")
        # Restart the listening process recursively or via loop
        listen_for_wake_word()

if __name__ == "__main__":
    try:
        listen_for_wake_word()
    except KeyboardInterrupt:
        print("Wake Engine stopped.")
