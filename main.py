from Frontend.Ui import UltronUI
from Backend.wakeword import WakeWordListener
from Backend.speech import SpeechManager
from Backend.ai import AIManager


class Ultron:
    def __init__(self):
        # -------------------------
        # UI
        # -------------------------

        self.ui = UltronUI()

        # Start hidden
        self.ui.hide()

        # -------------------------
        # Speech
        # -------------------------

        self.speech = SpeechManager()

        # -------------------------
        # AI
        # -------------------------

        self.ai = AIManager()

        # -------------------------
        # Wake Word
        # -------------------------

        self.wakeword = WakeWordListener(
            self.on_wake
        )

    # ==================================================
    # Wake word detected
    # ==================================================

    def on_wake(self):
        print("ULTRON ACTIVATED")

        # Tkinter must be updated from its own main thread
        self.ui.app.after(
            0,
            self.ui.show
        )

        # Start listening after UI activates
        self.ui.app.after(
            300,
            self.listen
        )

    # ==================================================
    # Listen
    # ==================================================

    def listen(self):
        print("ULTRON IS LISTENING")

        self.ui.set_status("LISTENING")

        # Record microphone
        audio_file = self.speech.listen(
            duration=6
        )

        if not audio_file:
            print("No audio recorded.")
            self.standby()
            return

        # -------------------------
        # Transcribe
        # -------------------------

        self.ui.set_status("THINKING")

        text = self.ai.transcribe(
            audio_file
        )

        # Delete temporary WAV
        self.speech.cleanup(
            audio_file
        )

        if text:
            print()
            print("====================")
            print("YOU SAID:")
            print(text)
            print("====================")
        else:
            print("Could not understand speech.")

        self.standby()

    # ==================================================
    # Standby
    # ==================================================

    def standby(self):
        self.ui.set_status("STANDBY")

        print("ULTRON READY")
        print("Waiting for wake word...")

    # ==================================================
    # Start Ultron
    # ==================================================

    def start(self):
        print("ULTRON v1.47")
        print("System started.")
        print("Waiting for wake word...")

        self.wakeword.start()

        self.ui.run()


# ======================================================
# Main
# ======================================================

if __name__ == "__main__":
    ultron = Ultron()
    ultron.start()