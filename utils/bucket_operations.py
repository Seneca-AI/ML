from google.cloud import storage
from glob import glob
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/home/sagar/Downloads/sagar-google-auth.json"

class bucketTransactions():
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket_name = bucket_name  # 'nayan_training_data'
        self.bucket = self.client.get_bucket(self.bucket_name)

    def upload_file_to_bucket(self, bucket_filename, local_filename):
        blob = self.bucket.blob(bucket_filename)
        blob.upload_from_filename(local_filename)

    def download_from_bucket(self, bucket_filename, local_filename):
        blob = self.bucket.blob(bucket_filename)
        blob.download_to_filename(local_filename)

    def list_objects(self):
        blobs = self.client.list_blobs(self.bucket_name)
        for blob in blobs:
            print(blob.name)

    def upload_folder_to_bucket(self, folder_path):
        for item in glob(folder_path+'/*'):
            print('folder : ', item)
            if os.path.isdir(item):
                self.upload_folder_to_bucket(item)
            elif os.path.isfile(item):
                blob = self.bucket.blob(item[1:])
                print(item)
                blob.upload_from_filename(item)  # local file_name
                print('uploaded to ', item[1:])
                
if __name__ == '__main__':              
    transaction = bucketTransactions('ml_dataflow')
    transaction.list_objects()