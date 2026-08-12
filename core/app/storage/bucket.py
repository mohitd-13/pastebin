from aiobotocore.client import AioBaseClient

from app.config import settings

BUCKET_NAME=settings.aws_s3_bucket_name


async def create_object(s3: AioBaseClient, bucket_key: str, content: bytes) -> None:
        """
        Store text content into s3 bucket
        """
        await s3.put_object(
                Bucket=BUCKET_NAME,
                Key=bucket_key,
                Body=content,
        )

async def read_object(s3: AioBaseClient, bucket_key: str) -> bytes:
        """
        Retrive bytes content from s3 bucket
        """
        response = await s3.get_object(
                Bucket=BUCKET_NAME,
                Key=bucket_key,
        )
        return await response["Body"].read()
        

async def delete_object(s3: AioBaseClient, bucket_key: str) -> None:
        """
        Delete content from s3 bucket
        """
        await s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=bucket_key,
        )
