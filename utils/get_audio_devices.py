#!/usr/bin/env python3
import pyaudio

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)

    # Ignore non-hardware devices
    if "hw" not in info['name']:
        continue

    print(info['name'])
    print("\tDevice index\t\t", info['index'])
    print("\tInput channels\t\t", info['maxInputChannels'])
    print("\tOutput channels\t\t", info['maxOutputChannels'])
    print("\tDefault samplerate\t", info['defaultSampleRate'])
