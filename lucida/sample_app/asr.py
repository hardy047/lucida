import speech_recognition as sr
import pyaudio
import wave
import httplib2
import urllib
import os
import time

from ThriftClient import thrift_client
from commandcenterlib.query_classifier import query_classifier
from commandcenterlib.utilities import log, check_image_extension

chunk = 2048
 
def get_audio(input_text):
    mary_host = "localhost"
    mary_port = "59125"
    query_hash = {"INPUT_TEXT": input_text,
              "INPUT_TYPE":"TEXT", # Input text
              "LOCALE":"en_US",
              "VOICE":"cmu-slt-hsmm", # Voice informations  (need to be compatible)
              "OUTPUT_TYPE":"AUDIO",
              "AUDIO":"WAVE", # Audio informations (need both)
              }
    query = urllib.urlencode(query_hash)
    h_mary = httplib2.Http()
    resp, content = h_mary.request("http://%s:%s/process?" % (mary_host, mary_port), "POST", query)
    if (resp["content-type"] == "audio/x-wav"):
        # Write the wav file.
        filename = 'output.wav'
        f = open(filename, "wb")
        f.write(content)
        f.close()
    return filename

def say(speech_input):
    os.system("aplay " + speech_input)
    #f = wave.open(speech_input,"rb")  
    #instantiate PyAudio  
    #p = pyaudio.PyAudio()  
    #open stream  
    #stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
    #                channels = f.getnchannels(),  
    #                rate = f.getframerate(),  
    #                output = True)  
    #read data  
    #data = f.readframes(chunk)  

    #paly stream  
    #while data != '':  
    #    stream.write(data)  
    #    data = f.readframes(chunk)  

    #stop stream  
    #stream.stop_stream()  
    #stream.close()  

    #close PyAudio  
    #p.terminate()

def listening(recognizer, audio):
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        speech_input = recognizer.recognize_google(audio)
        print("You said: " + speech_input)
        services_needed = query_classifier.predict(speech_input, None)
        result = thrift_client.infer('hardik', services_needed, speech_input, None)
        say(get_audio(result))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, listening)
# `stop_listening` is now a function that, when called, stops background listening

for _ in range(50): time.sleep(0.1) # we're still listening even though the main thread is doing other things
stop_listening() # calling this function requests that the background listener stop listening
while True: time.sleep(0.1)
