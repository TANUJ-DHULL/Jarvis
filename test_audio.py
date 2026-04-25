import pyaudio
import array
import math

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

def get_rms(data):
    shorts = array.array('h', data)
    sum_squares = sum(float(sample)**2 for sample in shorts)
    return math.sqrt(sum_squares / len(shorts)) if shorts else 0

def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Listening for 10 chunks to test volume...")
    for i in range(10):
        data = stream.read(CHUNK)
        print(f"RMS: {get_rms(data)}")
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    main()
