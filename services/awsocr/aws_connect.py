import logging
import boto3

from helpers.enum_aws_connect import EnumAwsConnect as const
from helpers.enviroment import AWS_BUCKET, SNS_TOPIC_ARN, ROLE_ARN
from botocore.exceptions import ClientError


class AwsConnect:
    def __init__(self):
        self.client = boto3.client(const.TEXT_EXTRACT.value)
        self.status = const.IN_PROGRESS.value
        self.response_status = None
        self.doc_name = None

    def ocr_object(self):
        response = self.client.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': AWS_BUCKET,
                    'Name': self.doc_name
                }
            },
            FeatureTypes=['FORMS'],
            ClientRequestToken="NKEY"+self.doc_name.split('.')[0],
            NotificationChannel={
                "SNSTopicArn": SNS_TOPIC_ARN,
                "RoleArn": ROLE_ARN
            },
            JobTag="Receipt"
        )
        while self.status == const.IN_PROGRESS.value:
            if const.NEXT_TOKEN.value in response.keys():
                self.response_status = self.client.get_document_analysis(
                    JobId=response[const.JOB_ID.value],
                    MaxResults=const.MAX_RESULTS.value,
                    NextToken=response[const.NEXT_TOKEN.value]
                )
            else:
                self.response_status = self.client.get_document_analysis(
                    JobId=response[const.JOB_ID.value],
                    MaxResults=const.MAX_RESULTS.value,
                )
            self.status = self.response_status[const.JOB_STATUS.value]
        return self.response_status

    def upload_file(self, file):
        self.doc_name = file.filename
        s3_client = boto3.client(const.BUCKET_S3.value)
        try:
            s3_client.put_object(Bucket=AWS_BUCKET, Key=file.filename, Body=file.read())
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def delete_object_s3(self):
        s3 = boto3.resource(const.BUCKET_S3.value)
        s3.Object(AWS_BUCKET, self.doc_name).delete()
