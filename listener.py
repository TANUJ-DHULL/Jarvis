import speech_recognition as sr
from speaker import speak

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            # Use hi-IN for Hindi (it also recognizes English words fairly well)
            query = r.recognize_google(audio, language='hi-IN')
            print(f"You said (Original): {query}")
            
            # Translate the recognized text to English to process commands
            from mtranslate import translate
            query_eng = translate(query, "en", "auto")
            print(f"Translated to English: {query_eng}\n")
            return query_eng.lower()
        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print("Say that again please...")
            return "none"
    return "none"

def listen_hinglish():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for Hinglish...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            print("Recognizing Hinglish...")
            # Use 'en-IN' to correctly capture Hinglish words
            query = r.recognize_google(audio, language='en-IN')
            print(f"You said (Hinglish): {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print("Say that again please...")
            return "none"
    return "none"

if __name__ == "__main__":
    print("Listening module test. Please speak.")
    text = listen()
    if text != "None":
        speak(f"You just said: {text}")
