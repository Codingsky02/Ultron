from Frontend.Ui import UltronUI
from Backend.wakeword import WakeWordListener
from Backend.speech import SpeechManager
from Backend.ai import AIManager
from Backend.tools import ToolManager

import winsound
import os
import subprocess
import threading
import time
import json


# ==================================================
# Configuration
# ==================================================

WAKE_WORD = "Hey Jarvis"

ACTIVATION_SOUND = (
    "Frontend/Static/Activation.wav"
)

ACTIVATION_DURATION = 6

STARTUP_GREETING = (
    "Good morning, sir. ULTRON is online and ready. "
    "Core functions initialized. Systems are operational. "
    "Awaiting your command."
)


class Ultron:

    def __init__(self):

        # -------------------------
        # UI
        # -------------------------

        self.ui = UltronUI()

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
        # Tools
        # -------------------------

        self.tools = ToolManager()

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

        self.play_activation_sound()

        self.ui.app.after(
            0,
            lambda: self.ui.set_status("SPEAKING")
        )

        self.speak(
            STARTUP_GREETING
        )

        elapsed = time.time() - sequence_start

        remaining = ACTIVATION_DURATION - elapsed

        if remaining > 0:

            time.sleep(
                remaining
            )

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

        self.ui.app.after(
            0,
            self.ui.show
        )

        if self.first_activation:

            self.first_activation = False

            threading.Thread(
                target=self.activation_sequence,
                daemon=True
            ).start()

        else:

            self.ui.app.after(
                300,
                self.listen
            )

    # ==================================================
    # Execute Command
    # ==================================================

    def execute_command(self, command_json):

        try:

            command = json.loads(
                command_json
            )

            action = command.get(
                "action"
            )

            print()
            print("====================")
            print("EXECUTING COMMAND")
            print(
                f"ACTION: {action}"
            )
            print("====================")

            # -------------------------
            # Open App
            # -------------------------

            if action == "open_app":

                target = command.get(
                    "target"
                )

                if not target:

                    return (
                        "I need to know which "
                        "application to open, sir."
                    )

                return self.tools.open_app(
                    target
                )

            # -------------------------
            # Open Website
            # -------------------------

            elif action == "open_website":

                target = command.get(
                    "target"
                )

                if not target:

                    return (
                        "I need to know which "
                        "website to open, sir."
                    )

                return self.tools.open_website(
                    target
                )

            # -------------------------
            # Get Time
            # -------------------------

            elif action == "get_time":

                return self.tools.get_time()

            # -------------------------
            # Get Date
            # -------------------------

            elif action == "get_date":

                return self.tools.get_date()

            # -------------------------
            # Set Volume
            # -------------------------

            elif action == "set_volume":

                level = command.get(
                    "level"
                )

                if level is None:

                    return (
                        "I need a volume level, sir."
                    )

                return self.tools.set_volume(
                    level
                )

            # -------------------------
            # Create Folder
            # -------------------------

            elif action == "create_folder":

                path = command.get(
                    "path"
                )

                if not path:

                    return (
                        "I need a folder path, sir."
                    )

                return self.tools.create_folder(
                    path
                )

            # -------------------------
            # Create File
            # -------------------------

            elif action == "create_file":

                path = command.get(
                    "path"
                )

                content = command.get(
                    "content",
                    ""
                )

                if not path:

                    return (
                        "I need a file path, sir."
                    )

                return self.tools.create_file(
                    path,
                    content
                )

            # -------------------------
            # Unknown
            # -------------------------

            elif action == "unknown":

                return (
                    "I'm not sure how to perform "
                    "that command yet, sir."
                )

            # -------------------------
            # Invalid Action
            # -------------------------

            else:

                return (
                    "That command is not available "
                    "in my current systems, sir."
                )

        except json.JSONDecodeError:

            print(
                "Invalid JSON returned by Gemini."
            )

            return (
                "I couldn't process that command, sir."
            )

        except Exception as error:

            print(
                f"Command execution error: {error}"
            )

            return (
                "An error occurred while executing "
                "that command, sir."
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

        # -------------------------
        # Record Microphone
        # -------------------------

        audio_file = self.speech.listen(
            duration=6
        )

        if not audio_file:

            print(
                "No audio recorded."
            )

            self.standby()

            return

        # -------------------------
        # Transcribe
        # -------------------------

        self.ui.set_status(
            "THINKING"
        )

        text = self.ai.transcribe(
            audio_file
        )

        # -------------------------
        # Cleanup Audio
        # -------------------------

        self.speech.cleanup(
            audio_file
        )

        if not text:

            print(
                "Could not understand speech."
            )

            self.standby()

            return

        print()
        print("====================")
        print("YOU SAID:")
        print(text)
        print("====================")

        # -------------------------
        # Interpret Command
        # -------------------------

        command = self.ai.interpret_command(
            text
        )

        if not command:

            print(
                "Gemini could not interpret command."
            )

            self.speak(
                "I couldn't understand that command, sir."
            )

            self.standby()

            return

        # -------------------------
        # Execute Command
        # -------------------------

        response = self.execute_command(
            command
        )

        print()
        print("====================")
        print("ULTRON RESPONSE:")
        print(response)
        print("====================")

        # -------------------------
        # Speak Response
        # -------------------------

        self.ui.set_status(
            "SPEAKING"
        )

        self.speak(
            response
        )

        # -------------------------
        # Standby
        # -------------------------

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