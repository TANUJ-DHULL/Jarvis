import pyttsx3

def speak(text):
    print(f"EDITH: {text}")
    engine = pyttsx3.init()
    # Optional: Configure voice and speed
    voices = engine.getProperty('voices')
    # Try to set a voice (0=default male, 1=female usually)
    if len(voices) > 0:
        engine.setProperty('voice', voices[0].id) 
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Speaker module is online.")
