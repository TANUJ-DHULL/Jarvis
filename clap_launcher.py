import json
import math
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pyaudio


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "clap_launcher_config.json"
LOG_PATH = BASE_DIR / "clap_listener_log.txt"
PROJECT_PYTHON = BASE_DIR / ".conda" / "python.exe"


DEFAULT_CONFIG = {
    "clap_threshold": 7000,
    "clap_window_seconds": 1.2,
    "cooldown_seconds": 8,
    "chunk_size": 1024,
    "sample_rate": 44100,
    "channels": 1,
    "jarvis_command": "",
}


def load_config():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
        return DEFAULT_CONFIG.copy()

    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        user_config = json.load(handle)

    config = DEFAULT_CONFIG.copy()
    config.update(user_config)
    return config


def log(message):
    stamp = time.strftime("%H:%M:%S")
    line = f"[{stamp}] {message}"
    print(line, flush=True)
    try:
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except Exception:
        pass


def calculate_rms(frame):
    if not frame:
        return 0

    count = len(frame) // 2
    if count <= 0:
        return 0

    total = 0
    for index in range(0, len(frame) - 1, 2):
        sample = int.from_bytes(frame[index:index + 2], byteorder="little", signed=True)
        total += sample * sample
    return int(math.sqrt(total / count))


def get_python_command():
    if PROJECT_PYTHON.exists():
        return str(PROJECT_PYTHON)
    return sys.executable


def guess_jarvis_command():
    candidates = [
        "start_jarvis.bat",
        "run_jarvis.bat",
        "launch_jarvis.bat",
        "jarvis.bat",
        "start.bat",
        "run.bat",
        "launch.bat",
        "main.py",
        "app.py",
        "jarvis.py",
    ]

    for name in candidates:
        target = BASE_DIR / name
        if not target.exists():
            continue
        if target.suffix.lower() == ".py":
            return f'"{get_python_command()}" "{target}"'
        return f'"{target}"'

    return ""


def resolve_command(config):
    configured = str(config.get("jarvis_command", "")).strip()
    if configured:
        return configured
    return guess_jarvis_command()


def run_jarvis(command):
    if not command:
        log("Jarvis command missing. Update clap_launcher_config.json")
        return

    creation_flags = 0
    if os.name == "nt":
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

    try:
        subprocess.Popen(
            command,
            cwd=str(BASE_DIR),
            shell=True,
            creationflags=creation_flags,
        )
        log("Double clap detected. Jarvis launch command sent.")
    except Exception as exc:
        log(f"Launch failed: {exc}")


def listen_for_double_clap():
    config = load_config()
    command = resolve_command(config)

    if command:
        log(f"Launch command: {command}")
    else:
        log("No launch command found. Waiting anyway until config is updated.")
    log(
        "Using threshold="
        f"{config['clap_threshold']} window={config['clap_window_seconds']}s cooldown={config['cooldown_seconds']}s"
    )

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=int(config["channels"]),
        rate=int(config["sample_rate"]),
        input=True,
        frames_per_buffer=int(config["chunk_size"]),
    )

    clap_times = []
    cooldown_until = 0.0

    try:
        log("Double clap listener active.")
        while True:
            frame = stream.read(int(config["chunk_size"]), exception_on_overflow=False)
            amplitude = calculate_rms(frame)
            now = time.time()

            if now < cooldown_until:
                continue

            if amplitude >= int(config["clap_threshold"]):
                clap_times = [t for t in clap_times if now - t <= float(config["clap_window_seconds"])]

                # Small debounce to reduce multiple hits from one clap.
                if clap_times and now - clap_times[-1] < 0.18:
                    continue

                clap_times.append(now)
                log(f"Clap heard: {len(clap_times)}/2")

                if len(clap_times) >= 2:
                    threading.Thread(target=run_jarvis, args=(command,), daemon=True).start()
                    clap_times.clear()
                    cooldown_until = now + float(config["cooldown_seconds"])
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def main():
    try:
        if LOG_PATH.exists():
            try:
                LOG_PATH.unlink()
            except Exception:
                pass
        listen_for_double_clap()
    except KeyboardInterrupt:
        log("Stopped.")
    except Exception as exc:
        log(f"Fatal error: {exc}")


if __name__ == "__main__":
    main()
