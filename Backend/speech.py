import sounddevice as sd
import soundfile as sf
import tempfile
import os


class SpeechManager:
    def __init__(self):
        # -------------------------
        # Audio settings
        # -------------------------

        self.sample_rate = 16000
        self.channels = 1

    # ==================================================
    # Speech → Audio
    # ==================================================

    def listen(self, duration=6):
        """
        Record microphone audio.

        Returns:
            str: Path to temporary WAV file
            None: If recording fails
        """

        print("LISTENING...")
        print("Speak now...")

        try:
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32"
            )

            sd.wait()

            # Temporary WAV file
            temp_file = tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            )

            temp_file.close()

            sf.write(
                temp_file.name,
                audio,
                self.sample_rate
            )

            print(f"Audio recorded: {temp_file.name}")

            return temp_file.name

        except Exception as error:
            print(f"Microphone error: {error}")
            return None

    # ==================================================
    # Cleanup
    # ==================================================

    def cleanup(self, file_path):
        """
        Delete a temporary audio file.
        """

        if file_path and os.path.exists(file_path):

            try:
                os.remove(file_path)

            except OSError:
                pass



