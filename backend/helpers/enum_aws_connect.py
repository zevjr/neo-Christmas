from enum import Enum


class EnumAwsConnect(Enum):
    TEXT_EXTRACT = "textract"
    IN_PROGRESS = "IN_PROGRESS"
    JOB_ID = "JobId"
    BUCKET_S3 = "s3"
    NEXT_TOKEN = "NextToken"
    JOB_STATUS = "JobStatus"
    MAX_RESULTS = 9999999999
