from service.awsocr.aws_connect import AwsConnect


class ExtractOcrData(AwsConnect):
    def __init__(self):
        super().__init__()
        self.data = None

    def run(self, file):
        self.get_ocr_data(file)
        print(self.data)
        return self.data

    def get_ocr_data(self, file):
        if self.upload_file(file):
            self.data = self.ocr_object()
            self.delete_object_s3()
            return True
        return False
