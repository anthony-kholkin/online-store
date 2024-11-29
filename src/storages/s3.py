import io
import os

import botocore.exceptions
from aioboto3.session import Session
from fastapi import Depends
from loguru import logger

from core.config import settings
from storages.base import BaseStorage, get_updated_path_depending_on_os
from storages.session import get_boto3_session


class S3Storage(BaseStorage):
    def __init__(self, boto3_session: Session = Depends(get_boto3_session)) -> None:
        self._boto3_session = boto3_session

        self._s3_endpoint_url = settings().S3_DSN
        self._s3_bucket_name = settings().S3_BUCKET_NAME

        self._storage_dsn = os.path.join(
            self._s3_endpoint_url,
            self._s3_bucket_name,
        )

    async def upload_file(self, key: str | None, data: bytes, content_type: str | None) -> str | None:
        if key is None:
            return None

        content = io.BytesIO(data)

        key = get_updated_path_depending_on_os(os.path.join(settings().STORAGE_FILE_PATH, key))

        try:
            async with self._boto3_session.client("s3", endpoint_url=self._s3_endpoint_url) as s3_client:
                await s3_client.upload_fileobj(
                    Fileobj=content,
                    Bucket=self._s3_bucket_name,
                    Key=key,
                    ExtraArgs={"ContentType": content_type},
                )

            return key

        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as e:
            logger.error(f"Unable to upload file {key}: {e}")
            return None

    async def delete_file(self, key: str | None) -> bool:
        if key is None:
            return False

        try:
            async with self._boto3_session.client("s3", endpoint_url=self._s3_endpoint_url) as s3_client:
                await s3_client.delete_object(Bucket=self._s3_bucket_name, Key=key)

            return True

        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as e:
            logger.error(f"Unable to delete file {key}: {e}")
            return False

    async def is_file_exists(self, key: str | None) -> bool:
        if key is None:
            return False

        try:
            async with self._boto3_session.client("s3", endpoint_url=self._s3_endpoint_url) as s3_client:
                await s3_client.head_object(Bucket=self._s3_bucket_name, Key=key)

            return True

        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as e:
            logger.error(f"Unable to get head object {key}: {e}")
            return False

    async def generate_presigned_url(
        self,
        key: str | None,
        method: str = "get_object",
        expires_in: int = settings().PRESIGNED_FILE_URL_EXPIRATION_TIME,
    ) -> str | None:
        if key is None:
            return None

        try:
            async with self._boto3_session.client("s3", endpoint_url=self._s3_endpoint_url) as s3_client:
                return await s3_client.generate_presigned_url(
                    method,
                    Params={"Bucket": self._s3_bucket_name, "Key": key},
                    ExpiresIn=expires_in,
                )

        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
        ) as e:
            logger.error(f"Unable to get head object {key}: {e}")
            return None

    def get_file_url(self, key: str | None) -> str | None:
        if key is None:
            return None

        return f"{self._storage_dsn}/{key}"
