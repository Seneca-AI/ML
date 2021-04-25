"""
cloud_storage_test tests all of the code in ml/cloud/google/cloud_storage_test
"""

import os
import unittest

from api.exceptions import MissingEnvironmentVariableError
from ml.cloud.google.cloud_storage import CloudStorageClient

class TestCloudStorage(unittest.TestCase):

    def test_environment_variables_set(self):
        with self.assertRaises(KeyError):
            CloudStorageClient()

        os.environ["GOOGLE_CLOUD_PROJECT"] = ""
        with self.assertRaises(MissingEnvironmentVariableError):
            CloudStorageClient()

        os.environ["GOOGLE_CLOUD_PROJECT"] = "my-project"

        with self.assertRaises(KeyError):
            CloudStorageClient()

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""
        with self.assertRaises(MissingEnvironmentVariableError):
            CloudStorageClient()

    # TODO(lucaloncar): consider testing download_to_file, or capture in integration test
