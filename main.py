from Frontend.Ui import UltronUI
from Backend.wakeword import WakeWordListener
from Backend.speech import SpeechManager
from Backend.ai import AIManager
import winsound
import os
import subprocess
import threading
import time


# ==================================================
# Configuration
# ==================================================

WAKE_WORD = "Hey Jarvis"

ACTIVATION_SOUND = (
    "Frontend/Static/Activation.wav"
)

ACTIVATION_DURATION = 6

STARTUP_GREETING = (
    "Good morning, sir. ULTRON is online and ready. Core functions initialized. Systems are operational. Awaiting your command."
)


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

        # -------------------------
        # First Activation
        # -------------------------

        self.first_activation = True

    # ==================================================
    # Activation Sound
    # ==================================================

    def play_activation_sound(self):

        try:

            sound_path = os.path.join(
                os.path.dirname(__file__),
                ACTIVATION_SOUND
            )

            winsound.PlaySound(
                sound_path,
                winsound.SND_FILENAME |
                winsound.SND_ASYNC
            )

        except Exception as error:

            print(
                f"Activation sound error: {error}"
            )

    # ==================================================
    # Text To Speech
    # ==================================================

    def speak(self, text):

        try:

            print(
                f"ULTRON SPEAKING: {text}"
            )

            # Escape characters that could
            # interfere with PowerShell.
            safe_text = (
                text
                .replace("'", "''")
                .replace("\n", " ")
            )

            command = [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                (
                    "Add-Type -AssemblyName System.Speech; "
                    "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                    "$speaker.Rate = 0; "
                    "$speaker.Volume = 100; "
                    f"$speaker.Speak('{safe_text}');"
                )
            ]

            subprocess.run(
                command,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

        except Exception as error:

            print(
                f"TTS error: {error}"
            )

    # ==================================================
    # Activation Sequence
    # ==================================================

    def activation_sequence(self):

        sequence_start = time.time()

        # ------------------------------------------
        # Start activation sound
        # ------------------------------------------

        self.play_activation_sound()

        # ------------------------------------------
        # Immediate local greeting
        # ------------------------------------------

        self.ui.app.after(
            0,
            lambda: self.ui.set_status("SPEAKING")
        )

        self.speak(
            STARTUP_GREETING
        )

        # ------------------------------------------
        # Make sure the activation sequence
        # lasts at least 6 seconds
        # ------------------------------------------

        elapsed = (
            time.time() - sequence_start
        )

        remaining = (
            ACTIVATION_DURATION - elapsed
        )

        if remaining > 0:

            time.sleep(
                remaining
            )

        # ------------------------------------------
        # Begin listening
        # ------------------------------------------

        self.ui.app.after(
            0,
            self.listen
        )

    # ==================================================
    # Wake Word Detected
    # ==================================================

    def on_wake(self):

        print(
            f"ULTRON ACTIVATED — {WAKE_WORD}"
        )

        # UI activates immediately
        self.ui.app.after(
            0,
            self.ui.show
        )

        # ------------------------------------------
        # First activation
        # ------------------------------------------

        if self.first_activation:

            self.first_activation = False

            # Run special activation sequence
            # in background so Tkinter does not freeze.
            threading.Thread(
                target=self.activation_sequence,
                daemon=True
            ).start()

        # ------------------------------------------
        # Normal activations
        # ------------------------------------------

        else:

            self.ui.app.after(
                300,
                self.listen
            )

    # ==================================================
    # Listen
    # ==================================================

    def listen(self):

        print(
            "ULTRON IS LISTENING"
        )

        self.ui.set_status(
            "LISTENING"
        )

        # ------------------------------------------
        # Record microphone
        # ------------------------------------------

        audio_file = self.speech.listen(
            duration=6
        )

        if not audio_file:

            print(
                "No audio recorded."
            )

            self.standby()

            return

        # ------------------------------------------
        # Transcribe
        # ------------------------------------------

        self.ui.set_status(
            "THINKING"
        )

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

            print(
                "Could not understand speech."
            )

        self.standby()

    # ==================================================
    # Standby
    # ==================================================

    def standby(self):

        self.ui.set_status(
            "STANDBY"
        )

        print(
            "ULTRON READY"
        )

        print(
            "Waiting for wake word..."
        )

    # ==================================================
    # Start Ultron
    # ==================================================

    def start(self):

        print(
            "ULTRON v1.47"
        )

        print(
            "System started."
        )

        print(
            "Waiting for wake word..."
        )

        self.wakeword.start()

        self.ui.run()


if __name__ == "__main__":

    ultron = Ultron()

    ultron.start()