#!/usr/bin/env python3
import argparse
import parallel
import time
import pyaudio
import wave

CHUNK = 1024

parser = argparse.ArgumentParser()
parser.add_argument(
    'device',
    action='store',
    type=int,
    help="Which audio device to test. Use the index given by utils/get_audio_devices.py"
)
parser.add_argument(
    '-t',
    '--times',
    action='store',
    type=int,
    default=4,
    required=False,
    help="How many times to run the test. Tests will be held with an interval of 1 second between tests"
)

arguments = parser.parse_args()

p = pyaudio.PyAudio()

print("Preparing test")

wf = wave.open('untitled.wav', 'rb')

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output_device_index=arguments.device,
                output=True)

port = parallel.Parallel()


for i in range(arguments.times):
    time.sleep(1)

    data = wf.readframes(CHUNK)

    print("Starting trial", i+1)

    port.setData(0x0)

    port.setData(0xFF)

    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)

    print("Finished, resetting")

    port.setData(0x0)

    wf.rewind()

stream.stop_stream()
stream.close()

p.terminate()
