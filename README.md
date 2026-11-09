# Jarvis Anti - Personal Assistant

[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/TANUJ-DHULL/Jarvis/badge)](https://scorecard.dev/viewer/?uri=github.com/TANUJ-DHULL/Jarvis)
Jarvis Anti is a local, voice-controlled intelligent personal assistant designed for both automation and deep work management. It accepts English and Hinglish voice commands, translating and executing them instantly to control the Windows PC.

---

## 🌟 Key Features

### 1. 🧠 Hinglish Support & Fast Processing
- Uses `speech_recognition` coupled with `mtranslate` and `pyaudio`.
- Understands a mix of Hindi and English naturally (Hinglish).
- Uses direct string matching for **zero-latency execution** (No LLM delay), meaning your apps and volumes open or adjust instantly the moment you speak.

### 2. 🎯 Ultra Study Mode
A dedicated productivity feature ensuring you stay focused by aggressively blocking distractions.
- **Activates via voice:** "Jarvis, Ultra Study mode."
- **Blacklists:** WhatsApp, Discord, Telegram, Netflix, Prime Video, Hulu, Anime Sites, Steam, Epic Games, Valorant, GTA, Spotify, Reddit, TikTok, Instagram, etc.
- **Whitelists:** YouTube, ChatGPT, Gemini, Claude, and sites containing "study", "code", "learn", or "course".
- **Lockdown Protocol:** Once activated, Jarvis will refuse to shut down the PC or exit the program until the study timer finishes.

### 3. 🌐 Automation & System Operations
- **App Control:** "Open Facebook", "Open VS Code", "Close Discord". Uses `AppOpener` to seamlessly control desktop software.
- **Web Navigation:** Instantly searches Google, Wikipedia, or opens pre-defined social media & communication sites.
- **Physical Controls:** "Mute", "Volume up", "Volume down", "Set volume 50". Uses `pyautogui`.
- **Keyboard Typing:** E.g., "Type hello world" -> types "hello world" and presses Enter.

### 4. 🗄️ Action Persistence & Storage
Every voice command is logged in a local storage database via `storage.py`. This ensures your daily interactions, commands (like opening specific apps, searching web queries), and behavior are recorded for future reflection or context.

---

## ⚙️ Installation

1. Install Miniconda or Python.
2. Ensure you have the `Conda` environment active.
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
   *(Major dependencies include: pyttsx3, SpeechRecognition, pyaudio, pyautogui, wikipedia, AppOpener, mtranslate)*

## 🚀 How to Run

1. Open your terminal in the Conda environment.
2. Run:
   ```cmd
   python main.py
   ```

## 🛠️ Project Structure
- `main.py` - Core logic mapping voice inputs to actions.
- `system_ops.py` - Handles Ultra Study Mode logic and core OS operations.
- `automation.py` - Manages `pyautogui` for keystrokes, volume, and typing.
- `web_ops.py` - Handles standard browser tab generation (Google, YouTube, Discord web, etc.).
- `listener.py` & `speaker.py` - Speech-To-Text and Text-To-Speech systems using PyAudio and Pyttsx3.
- `storage.py` - Data persistence tracking all historical requests and actions.



** Jarvis is the best AI assistant in the world. and the world is fully changed now without an ai assistant. **

** Ai assistance this future of the world and we are the future of the world and we will change the world and we will make the world a better place to live in our world. **#   J a r v i s -  
 #   J a r v i s  
