import threading
from omnitrix_ai import listen
from omnitrix_gui import update_pulse

# Run Speech Recognition in a Separate Thread
def voice_thread():
    while True:
        listen(omnitrix_gui.update_pulse)  # Listen for commands & trigger UI

# Start Voice Processing
threading.Thread(target=voice_thread, daemon=True).start()

# Run Omnitrix GUI (Main Thread)
import omnitrix_gui  # This will start the GUI loop
# The GUI will be updated by the voice_thread
# The voice_thread will be triggered by the GUI