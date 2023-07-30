# SPEECH RECOGNITION
import speech_recognition as sr

# START API
r = sr.Recognizer()
filename = "msg6342383709-5665.wav"

# open the file
with sr.AudioFile(filename) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data)
    print(text)