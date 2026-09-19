from Backend.speech import SpeechManager
from Backend.ai import AIManager


speech = SpeechManager()
ai = AIManager()


# Record voice
audio_file = speech.listen(duration=6)

if audio_file:

    # Convert voice → text
    text = ai.transcribe(audio_file)

    print()
    print("====================")
    print("YOU SAID:")
    print(text)
    print("====================")

    # Delete temporary WAV
    speech.cleanup(audio_file)