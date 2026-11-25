'''import speech_recognition as sr
import pyttsx3
import webbrowser
#recognizer objext
recognizer=sr.Recognizer()
engine=pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()
def processComand():
     pass
if __name__=="__main__":
    speak("initialixing jarvis")
    '''
import pyttsx3

engine = pyttsx3.init()
engine.say("Hello Rajesh")
engine.runAndWait()
