import threading
import numpy as np
import sounddevice as sd
from openwakeword.model import Model


class WakeWordListener:
    def __init__(self, on_wake):
        self.on_wake = on_wake
        self.running = False
        self.thread = None

        # Temporary wake word for testing.
        # We will replace this with the custom "Ultron" model later.
        self.model = Model(
            wakeword_models=[
                "hey_jarvis"
            ]
        )

    def start(self):
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._listen,
            daemon=True
        )

        self.thread.start()

        print("Wake-word listener started.")
        print('Say "Hey Jarvis" to wake Ultron.')

    def stop(self):
        self.running = False

    def _listen(self):
        sample_rate = 16000
        block_size = 1280

        try:
            with sd.InputStream(
                samplerate=sample_rate,
                channels=1,
                dtype="int16",
                blocksize=block_size
            ) as stream:

                while self.running:
                    audio, _ = stream.read(block_size)

                    audio = np.squeeze(audio)

                    prediction = self.model.predict(audio)

                    score = prediction.get(
                        "hey_jarvis",
                        0
                    )

                    if score > 0.5:
                        print("Wake word detected!")

                        self.on_wake()

                        # Prevent repeated triggers
                        self.model.reset()

        except Exception as e:
            print(f"Wake-word error: {e}")
            self.running = False

