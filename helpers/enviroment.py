import os

from dotenv import load_dotenv

load_dotenv()

AWS_BUCKET = os.getenv("AWS_BUCKET")
SNS_TOPIC_ARN = os.getenv("SNSTOPICARN")
ROLE_ARN = os.getenv("ROLEARN")
URL_MONGO_DB = os.getenv("URL_MONGO_DB")
PORT_MONGO_DB = int(os.getenv("PORT_MONGO_DB"))
API_KEY = os.getenv("API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
