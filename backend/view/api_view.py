import time
from flask import jsonify, request

from backend.services.speech_to_text.convert_speech_to_text import SpeechToText


def transcribe_audio_to_text():
    content = SpeechToText().run(request.files['file'])
    return jsonify({'status': 'success', 'content': content})
