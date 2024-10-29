from rest_api.services.s3 import ObjectStorageService


class CdnStorage(ObjectStorageService):
    def gen_upload_url(self, file_name: str) -> str:
        return self.generate_presigned_url(
            "put_object",
            {"Bucket": self.bucket_name, "Key": file_name, "ACL": "public-read"},
            self.DEFAULT_EXPIRATION,
        )

    def gen_download_url(self, file_name: str) -> str:
        return f"{self.endpoint_url}/{self.bucket_name}/{file_name}"
