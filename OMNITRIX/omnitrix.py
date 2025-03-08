import pygame
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import threading

# ========== SET UP GEMINI AI ==========
API_KEY = "AIzaSyC5hmkjhZknvBHVnxXwavOie7BiJLYR8Vc"  # Replace with your actual key
genai.configure(api_key=API_KEY)

try:
    chat = genai.GenerativeModel("gemini-2.0-pro-exp-02-05").start_chat()  # Corrected model initialization
except Exception as e:
    print(f"⚠ Gemini API Initialization Error: {e}")
    chat = None

# ========== SET UP TEXT-TO-SPEECH ==========
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Adjust speech speed

# Ensure voice is set properly
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change index if needed

stop_speaking = threading.Event()  # Flag to stop speaking

def speak(text):
    """Convert text to speech and allow interruptions."""
    def _speak():
        stop_speaking.clear()  # Reset flag before speaking
        update_pulse(True)  # Start pulsing while speaking
        draw_gui()

        engine.say(text)
        engine.runAndWait()  # Ensure it actually speaks

        update_pulse(False)  # Stop pulsing after speaking
        draw_gui()

    threading.Thread(target=_speak, daemon=True).start()

# ========== SET UP SPEECH RECOGNITION ==========
def recognize_speech():
    """Continuously listen for voice commands and interrupt speech if needed."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("🎤 Listening... (Speak Now)")
            update_pulse(True)  # Start pulsing while listening
            draw_gui()

            try:
                audio = recognizer.listen(source, timeout=5)
                stop_speaking.set()  # Interrupt speech if user talks
                update_pulse(False)  # Stop pulsing after listening
                draw_gui()

                user_input = recognizer.recognize_google(audio).lower()
                print(f"🗣 You said: {user_input}")
                process_command(user_input)
            except sr.UnknownValueError:
                print("⚠ Could not understand audio")
            except sr.RequestError:
                print("⚠ Speech Recognition API error")
            except Exception as e:
                print(f"⚠ Error: {e}")

# ========== PROCESS COMMAND ==========
def process_command(user_input):
    """Process user input and get Gemini AI response."""
    if not chat:
        print("⚠ Gemini API is not initialized. Check API key.")
        speak("I cannot access the AI. Please check my configuration.")
        return

    try:
        response = chat.send_message(user_input).text
        print(f"🤖 Omnitrix AI: {response}")
        speak(response)
    except Exception as e:
        print(f"⚠ Gemini API Error: {str(e)}")
        speak("Sorry, I couldn't process that.")

# ========== SET UP PYGAME UI ==========
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OMNITRIX AI")

# Load and resize Omnitrix image
omnitrix_img = pygame.image.load("omnitrix.png")
omnitrix_img = pygame.transform.scale(omnitrix_img, (200, 200))

# Omnitrix Symbol Position
x, y = (WIDTH // 2 - 100, HEIGHT // 2 - 100)

# UI Pulse Animation
pulse = False
pulse_size = 0  # Size of the animated pulse

def update_pulse(state):
    """Controls the pulsing animation state."""
    global pulse, pulse_size
    pulse = state
    pulse_size = 50 if state else 0  # Start pulse size when active

def draw_gui():
    """Draw Omnitrix UI and pulse animation."""
    global pulse_size
    screen.fill((0, 0, 0))  # Black background

    # Dynamic pulsing effect
    if pulse:
        for i in range(5):
            pygame.draw.circle(
                screen,
                (0, 255, 0, max(255 - (i * 50), 0)),  # Fading effect
                (WIDTH // 2, HEIGHT // 2),
                pulse_size + (i * 15),  # Bigger circles
                3  # Thickness
            )
        pulse_size += 3  # Gradually increase pulse size

        if pulse_size > 150:
            pulse_size = 50  # Reset pulse size to loop animation

    screen.blit(omnitrix_img, (x, y))  # Draw Omnitrix symbol
    pygame.display.update()

# ========== MAIN FUNCTION ==========
def main():
    threading.Thread(target=recognize_speech, daemon=True).start()  # Run voice recognition in background

    running = True
    while running:
        draw_gui()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
