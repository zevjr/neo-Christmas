from flask import render_template, request

from services.speech_to_text.convert_speech_to_text import SpeechToText


def transcribe_audio_to_text():
    content = SpeechToText().run(request.files['file'])
    return render_template("transcript.html", content=content)
