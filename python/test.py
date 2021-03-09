import parallel

import pyaudio
import wave

CHUNK = 1024

p = pyaudio.PyAudio()
wf = wave.open('untitled.wav', 'rb')

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output_device_index=9,
                output=True)

data = wf.readframes(CHUNK)

port = parallel.Parallel()

print("starting")

port.setData(0x0)

port.setData(0xFF)

while data != b'':
    stream.write(data)
    data = wf.readframes(CHUNK)

port.setData(0x0)

stream.stop_stream()
stream.close()

p.terminate()
