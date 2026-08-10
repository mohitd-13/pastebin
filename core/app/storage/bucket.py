import boto3

from core.app.config import settings

BUCKET_NAME=settings.aws_s3_bucket_name

session = boto3.Session(profile_name="pastebin")
s3 = session.client("s3")

def create_object(bucket_key: str, content: bytes) -> None:
        """
        Store text content into s3 bucket
        """
        s3.put_object(
                Bucket=BUCKET_NAME,
                Key=bucket_key,
                Body=content,
        )

def read_object(bucket_key: str) -> bytes:
        """
        Retrive bytes content from s3 bucket
        """
        response = s3.get_object(
                Bucket=BUCKET_NAME,
                Key=bucket_key,
        )
        return response["Body"].read()
        

def delete_object(bucket_key: str) -> None:
        """
        Delete content from s3 bucket
        """
        s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=bucket_key,
        )
