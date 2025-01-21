import boto3;
import json
import datetime
from .constants import DATE_FORMAT,S3_BUCKET_NAME,SQS_URL,SQS_NAME,SCRAPED_DATA_DIRECTORY_NAME
from models import MarketDataModel

s3_client = boto3.client('s3')

def upload_to_s3(filename : str,upload_data : list[MarketDataModel], rundate : datetime):
    if(upload_data.__len__() == 0):
        print("Empty News Data File, Not uploaded to S3 bucket --Skipping!")
        return ;
    
    json_data = json.dumps([data.__dict__ for data in upload_data], indent=4)

    print("Uploading to S3 bucket")

    bucket_name = S3_BUCKET_NAME 
    file_name = SCRAPED_DATA_DIRECTORY_NAME + rundate.strftime(DATE_FORMAT) + f"/{filename}.json"
    file_content = json_data
    
    try:
        # Upload the file to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_content
        )
        return {
            "statusCode": 200,
            "body": json.dumps(f"File {file_name} successfully uploaded to bucket {bucket_name}")
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error uploading file: {str(e)}")
        }
    

def produce_event_to_SQS(rundate : datetime):
    try:
        message = {
            "directory" : SCRAPED_DATA_DIRECTORY_NAME + rundate.strftime(DATE_FORMAT) + "/",
            "s3bucket" : S3_BUCKET_NAME,
            "rundate" : rundate.strftime(DATE_FORMAT),
            "event_type" : "daily"
        }
        sqs_client = boto3.client('sqs')

        sqs_client.send_message(
            QueueUrl = SQS_URL,
            MessageBody = json.dumps(message),
            MessageGroupId = rundate.strftime(DATE_FORMAT)
        )
        print("Message sent to SQS Queue ", SQS_NAME)
    except Exception as e:
        print("Error sending message to SQS Queue: ", str(e))




