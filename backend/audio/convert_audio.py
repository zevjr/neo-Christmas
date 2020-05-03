import requests
from backend.helpers.enviroment import API_KEY, AWS_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION


class ConvertAudio:
    def __init__(self, filename, format_in, format_out):
        self.filename_pay, self.payload, self.headers = 3 * [None]
        self.filename, self.format_in, self.format_out = filename, format_in, format_out

    def run(self):
        job_id = self.send_audio_to_convert()
        convert_id = self.convert_audio_any_format(job_id)
        return self.send_audio_converted_from_s3(convert_id)

    def send_audio_to_convert(self):
        url = "https://api.cloudconvert.com/v2/import/s3"
        self.filename_pay = self.filename + "." + self.format_in
        self.payload = "{\n\t\"access_key_id\": \"%s\",\n\t\"secret_access_key\": \"%s\",\n\t\"bucket\": \"%s\",\n\t\"region\": \"%s\",\n\t\"key\":\"%s\",\n\t\"filename\": \"%s\"\n}" % ( AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET, AWS_DEFAULT_REGION, self.filename_pay, self.filename_pay)
        self.headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=self.headers, data=self.payload).json()
        return response['data']['id']

    def convert_audio_any_format(self, job_id):
        url = "https://api.cloudconvert.com/v2/convert"
        payload = "{\n  \"input\": \"%s\",\n  \"input_format\": \"%s\",\n  \"output_format\": \"%s\"\n}" % (job_id, self.format_in, self.format_out)
        response = requests.post(url, headers=self.headers, data=payload).json()

        return response['data']['id']

    def send_audio_converted_from_s3(self, convert_id):
        url = "https://api.cloudconvert.com/v2/export/s3"
        self.filename_pay = self.filename + "." +self.format_out
        self.payload = "{\n\t\"input\": \"%s\",\n\t\"access_key_id\": \"%s\",\n\t\"secret_access_key\": \"%s\",\n\t\"bucket\": \"%s\",\n\t\"region\": \"%s\",\n\t\"key\":\"%s\",\n\t\"filename\": \"%s\"\n}" % (convert_id, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET, AWS_DEFAULT_REGION, self.filename_pay, self.filename_pay)

        response = requests.post(url, headers=self.headers, data=self.payload).json()

        return response
