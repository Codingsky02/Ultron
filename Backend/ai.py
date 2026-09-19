import os

from dotenv import load_dotenv
from google import genai


class AIManager:
    def __init__(self):
        # -------------------------
        # Load environment
        # -------------------------

        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        # -------------------------
        # Gemini client
        # -------------------------

        self.client = genai.Client(
            api_key=api_key
        )

    # ==================================================
    # Audio → Text
    # ==================================================

    def transcribe(self, audio_file):
        """
        Convert a WAV audio file into text.
        """

        try:
            print("TRANSCRIBING...")

            # Upload the audio file
            uploaded_file = self.client.files.upload(
                file=audio_file
            )

            # Use Gemini Interactions API
            interaction = self.client.interactions.create(
                model="gemini-3.6-flash",
                input=[
                    {
                        "type": "text",
                        "text": (
                            "Generate a transcript of the speech. "
                            "Return only the spoken words. "
                            "Do not add explanations."
                        )
                    },
                    {
                        "type": "audio",
                        "uri": uploaded_file.uri,
                        "mime_type": uploaded_file.mime_type
                    }
                ]
            )

            text = interaction.output_text.strip()

            print(f"HEARD: {text}")

            return text

        except Exception as error:
            print(f"Transcription error: {error}")
            return None