from Backend.speech import SpeechManager


speech = SpeechManager()

audio_file = speech.listen()

if audio_file:
    print("SUCCESS!")
    print("Recorded:", audio_file)

    speech.cleanup(audio_file)
    print("Temporary file deleted.")