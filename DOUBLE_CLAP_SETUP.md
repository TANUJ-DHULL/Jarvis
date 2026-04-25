# Double Clap Jarvis Setup

This adds a background listener that opens Jarvis when you clap twice.

## Files

- `clap_launcher.py`: microphone listener and launcher
- `clap_launcher_config.json`: sensitivity and launch command
- `Start-DoubleClapJarvis.bat`: starts the listener in background

## Install

1. Install Python 3 on Windows.
2. Install the audio packages:

```powershell
pip install pyaudio
```

If `pyaudio` fails, install with:

```powershell
py -m pip install pipwin
py -m pipwin install pyaudio
```

## Configure

Open `clap_launcher_config.json`.

If auto-detect does not find your Jarvis launcher, set:

```json
"jarvis_command": "\"C:\\Path\\To\\your-launcher.bat\""
```

Examples:

```json
"jarvis_command": "\"C:\\Jarvis Anti\\start.bat\""
```

```json
"jarvis_command": "\"C:\\Users\\Tanuj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe\" \"C:\\Jarvis Anti\\main.py\""
```

## Start

Double-click `Start-DoubleClapJarvis.bat`.

Then keep the microphone available. When you clap twice quickly, Jarvis will launch.

## One-Click Windows Startup

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\Install-DoubleClapStartup.ps1
```

This creates a Startup shortcut so the listener starts automatically after login.

## Tune Sensitivity

- Increase `clap_threshold` if normal room noise triggers it.
- Decrease `clap_threshold` if claps are not detected.
- `clap_window_seconds` controls how quickly the two claps must happen.

## Auto Start With Windows

Manual method: put a shortcut of `Start-DoubleClapJarvis.bat` into:

`shell:startup`

That makes the double clap listener start every time Windows logs in.
