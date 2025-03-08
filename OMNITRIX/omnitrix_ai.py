import pyttsx3
import speech_recognition as sr
import time

engine = pyttsx3.init()

# Function to Speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to Listen & Trigger UI
def listen(callback):
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening . . .")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")

        # Notify GUI to start pulsing
        callback(True)  
        time.sleep(1.5)  # Keep animation for a while
        callback(False) 

        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        return "Could not request results"

# Example usage (will be connected to the main program)
if __name__ == "__main__":
    listen(lambda x: print("GUI should react:", x))
    speak("Hello, I am OMNITRIX AI")
    speak("How can I help you?")