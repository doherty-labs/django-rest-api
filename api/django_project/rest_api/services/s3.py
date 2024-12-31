import boto3

from django_project import settings


class ObjectStorageService:
    DEFAULT_EXPIRATION = settings.OBJECT_EXPIRATION

    def __init__(
        self,
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        endpoint_url: str,
        region_name: str,
    ):
        self.bucket_name = bucket_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.region_name = region_name

    def get_s3_client(self):
        return boto3.client(
            "s3",
            aws_access_key_id=settings.BUCKET_KEY,
            aws_secret_access_key=settings.BUCKET_SECRET,
            endpoint_url=settings.BUCKET_ENDPOINT,
            region_name=settings.BUCKET_REGION,
        )

    def generate_presigned_url(
        self,
        client_method,
        method_parameters,
        expires_in,
    ) -> str:
        return self.get_s3_client().generate_presigned_url(
            ClientMethod=client_method,
            Params=method_parameters,
            ExpiresIn=expires_in,
        )

    def gen_upload_url(self, file_name: str) -> str:
        return self.generate_presigned_url(
            "put_object",
            {"Bucket": self.bucket_name, "Key": file_name},
            self.DEFAULT_EXPIRATION,
        )

    def gen_download_url(self, file_name: str) -> str:
        return self.generate_presigned_url(
            "get_object",
            {"Bucket": self.bucket_name, "Key": file_name},
            self.DEFAULT_EXPIRATION,
        )

    def delete_object(self, file_name: str) -> None:
        self.get_s3_client().delete_object(Bucket=self.bucket_name, Key=file_name)
