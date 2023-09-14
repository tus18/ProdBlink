import sys
import wave
import pyaudio

args = sys.argv
wf = wave.open(str(args[1])+".wav", "r")
chunk = 1024
data = wf.readframes(chunk)
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

while data != b'':
    stream.write(data)
    data = wf.readframes(chunk)
    
stream.close()
p.terminate()