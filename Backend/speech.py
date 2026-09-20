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

        temp_file_path = None

        try:
            # -------------------------
            # Record microphone
            # -------------------------

            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32"
            )

            sd.wait()

            # -------------------------
            # Create temporary WAV
            # -------------------------

            temp_file = tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            )

            temp_file_path = temp_file.name
            temp_file.close()

            # -------------------------
            # Save recording
            # -------------------------

            sf.write(
                temp_file_path,
                audio,
                self.sample_rate
            )

            print(
                f"Audio recorded: {temp_file_path}"
            )

            return temp_file_path

        except Exception as error:

            print(
                f"Microphone error: {error}"
            )

            # -------------------------
            # Cleanup failed recording
            # -------------------------

            if (
                temp_file_path
                and os.path.exists(temp_file_path)
            ):
                try:
                    os.remove(temp_file_path)

                except OSError:
                    pass

            return None

    # ==================================================
    # Cleanup
    # ==================================================

    def cleanup(self, file_path):
        """
        Delete a temporary audio file.
        """

        if not file_path:
            return

        if not os.path.exists(file_path):
            return

        try:

            os.remove(file_path)

            print(
                f"Audio cleanup complete: {file_path}"
            )

        except OSError as error:

            print(
                f"Audio cleanup error: {error}"
            )