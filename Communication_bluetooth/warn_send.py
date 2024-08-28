from vosk import Model, KaldiRecognizer
import pyaudio

model = Model(r"/home/cbpl/Downloads/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()


import socket

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect(("38:d5:7a:36:10:1c", 4))

print(f"Connected!")

def send(message):
    client.send(message.encode('utf-8'))


def Listen():
    print("")
    print("Listening...")
    print("")

    while True:

        data = stream.read(4096)

        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            p = text[14:-3]
            print(f"You Said : {p}")

            x=p.split()
                
            send(p)

            warn=""

            if "help" in x:
                warn="<HELP> detected"
                send(warn)
            elif "water" in x:
                warn="<WATER> detected"
                send(warn)
            elif "oxygen" in x:
                warn="<OXYGEN> detected"
                send(warn)
            elif "close" in x:
                break


            if len(p)>0:
                return p
            
            else:
                break

while(True):
    Listen()