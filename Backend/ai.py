import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai


class AIManager:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(
            api_key=api_key
        )

    # ==================================================
    # Generate Greeting
    # ==================================================

    def generate_greeting(self):

        try:

            current_hour = datetime.now().hour

            if 5 <= current_hour < 12:
                time_of_day = "morning"

            elif 12 <= current_hour < 17:
                time_of_day = "afternoon"

            elif 17 <= current_hour < 21:
                time_of_day = "evening"

            else:
                time_of_day = "night"

            print("GENERATING GREETING...")

            prompt = f"""
You are ULTRON, a sophisticated personal AI assistant.

The current time of day is {time_of_day}.

Generate a short, cinematic greeting for the user.

Requirements:
- Address the user as "sir"
- Sound intelligent, calm and futuristic
- Give a brief system-status style summary
- Make it feel like ULTRON has just come online
- Do not sound overly enthusiastic
- Do not mention that you are Gemini
- Do not use emojis
- Maximum 25 words
- Return ONLY the words that should be spoken aloud

Example style:
"Good afternoon, sir. ULTRON is online, systems are ready, and I am standing by for your command."
"""

            interaction = self.client.interactions.create(
                model="gemini-3.6-flash",
                input=[
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            )

            greeting = interaction.output_text.strip()

            print(
                f"GREETING: {greeting}"
            )

            return greeting

        except Exception as error:

            print(
                f"Greeting error: {error}"
            )

            return (
                "Good day, sir. ULTRON is online and ready."
            )

    # ==================================================
    # Transcription
    # ==================================================

    def transcribe(self, audio_file):

        try:

            print("TRANSCRIBING...")

            uploaded_file = self.client.files.upload(
                file=audio_file
            )

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

            print(
                f"HEARD: {text}"
            )

            return text

        except Exception as error:

            print(
                f"Transcription error: {error}"
            )

            return None

    # ==================================================
    # Interpret Command
    # ==================================================

    def interpret_command(self, text):

        try:

            print("ANALYZING COMMAND...")

            prompt = f"""
You are ULTRON, a Windows AI assistant.

Your job is to understand the user's command and return
ONLY valid JSON.

Available actions:

1. open_app

Example:
User: Open Chrome

JSON:
{{
    "action": "open_app",
    "target": "chrome"
}}


2. open_website

Example:
User: Open YouTube

JSON:
{{
    "action": "open_website",
    "target": "youtube.com"
}}


3. get_time

Example:
User: What time is it?

JSON:
{{
    "action": "get_time"
}}


4. get_date

Example:
User: What's today's date?

JSON:
{{
    "action": "get_date"
}}


5. set_volume

Example:
User: Set volume to 50 percent

JSON:
{{
    "action": "set_volume",
    "level": 50
}}


6. create_folder

Example:
User: Create a folder called Projects

JSON:
{{
    "action": "create_folder",
    "path": "Projects"
}}


7. create_file

Example:
User: Create a file called main.py inside Projects

JSON:
{{
    "action": "create_file",
    "path": "Projects/main.py",
    "content": ""
}}


Rules:

- Return ONLY valid JSON.
- Never return Python code.
- Never return PowerShell commands.
- Never explain anything.
- Use only the available actions.
- Do not invent new actions.
- If the command cannot be handled, return:

{{
    "action": "unknown"
}}

User command:
{text}
"""

            interaction = self.client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt
            )

            result = interaction.output_text.strip()

            print(
                f"COMMAND JSON: {result}"
            )

            return result

        except Exception as error:

            print(
                f"Command interpretation error: {error}"
            )

            return None