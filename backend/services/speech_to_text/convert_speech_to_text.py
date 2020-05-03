import requests
import random
import time
import boto3

from backend.audio.convert_audio import ConvertAudio
from backend.services.awsocr.aws_connect import AwsConnect


class SpeechToText(AwsConnect):
    def __init__(self):
        super().__init__()
        self.file_out, self.job_uri, self.file, self.job_name, self.media = 5*[None]

    def run(self, file):
        self.file = file
        self.file_out = "mp3"
        filename_out = self.file.filename.split(".")[0]+"."+self.file_out
        self.job_uri = f"https://speechtotextuniversity.s3.amazonaws.com/{filename_out}"
        self.job_name, self.media = self.file.filename.split(".")
        self.job_name = self.job_name + str(random.randrange(111111111, 999999999999))
        try:
            if self.upload_file(self.file) and self.file_out in self.media:
                return self.start_converting()
            else:
                resp = ConvertAudio(file.filename.split(".")[0], self.media, self.file_out).run()
                if "id" in resp.keys():
                    print(f"Arquivo convertido com sucesso de {self.media} para {self.file_out}")
                return self.start_converting()
        except Exception as e:
            print(e)
        finally:
            print([filename_out, self.file.filename])
            self.delete_object_s3([filename_out, self.file.filename])

    def start_converting(self):
        response = self.convert_speech_to_text()
        url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        resp = requests.get(url)
        resp = resp.json()
        return resp["results"]["transcripts"][0]["transcript"]

    def convert_speech_to_text(self):
        transcribe = boto3.client('transcribe')
        time.sleep(16)
        transcribe.start_transcription_job(
            TranscriptionJobName=self.job_name,
            Media={'MediaFileUri': self.job_uri},
            MediaFormat=self.file_out,
            LanguageCode='pt-BR'
        )
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=self.job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            time.sleep(15)
        return status