"""
cloud_storage provides a client for interfacing with Google Cloud Storage.
"""

import os
import tempfile

from google.cloud import storage

from api.exceptions import MissingEnvironmentVariableError
from api.constants import TMP_FILE_LOCATION

# pylint: disable=too-few-public-methods
class CloudStorageClient:
    """
    CloudStorageClient is the client for interfacing with Google Cloud Storage.
    """
    # TODO(lucaloncar): consider taking environment variables as parameters instead
    def __init__(self):
        if os.environ["GOOGLE_CLOUD_PROJECT"] == "":
            raise MissingEnvironmentVariableError("GOOGLE_CLOUD_PROJECT not set")

        if os.environ["GOOGLE_APPLICATION_CREDENTIALS"] == "":
            raise MissingEnvironmentVariableError("GOOGLE_APPLICATION_CREDENTIALS not set")

        # TODO(lucaloncar): pass the credentials here
        self.storage_client = storage.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])


    def download_file(self, url: str) -> str:
        """
        download_file downloads the Google Cloud Storage file with the give gsutil URI
        to a local tmp file on disk, and returns the path to the file

        Params:
            url string: the url of the file to download
        Returns:
            string: the path to the temp file on disk
        """
        try:
            # pylint: disable=consider-using-with
            temp_file = tempfile.NamedTemporaryFile(
                dir=TMP_FILE_LOCATION, suffix=".mp4", delete=False)
            blob = storage.Blob.from_string(url, client=self.storage_client)
            blob.download_to_filename(temp_file.name)
        finally:
            temp_file.close()
        return temp_file.name
    