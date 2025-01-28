import os
import datetime
import speech_recognition as sr
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("I'm listening. Please speak now.")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            return listen()

def create_voice_note():
    today_date = datetime.date.today().strftime("%Y-%m-%d")
    folder_path = os.path.join(os.getcwd(), "VoiceNotes", today_date)
    os.makedirs(folder_path, exist_ok=True)

    speak("What would you like to name this voice note?")
    note_name = listen()
    if not note_name:
        note_name = f"voice_note_{int(datetime.datetime.now().timestamp())}"

    file_path = os.path.join(folder_path, f"{note_name}.txt")

    speak("Start dictating your note. Say 'stop note' when you're done.")
    with open(file_path, "w") as file:
        while True:
            content = listen()
            if "stop note" in content:
                speak("Voice note saved successfully.")
                break
            else:
                file.write(content + "\n")

    print(f"Voice note saved at {file_path}")

def main():
    speak("Welcome to the voice note creator. Say 'create note' to begin or 'exit' to quit.")
    while True:
        command = listen()
        if "create note" in command:
            create_voice_note()
        elif "exit" in command:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    main()
