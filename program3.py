# import boto3
# import os
# import sys

# client = boto3.client('s3')
# local_path = "C:/Users/parth/Downloads/test"
# bucketname = "pmalladi-program3"

# for path, dirs, files in os.walk(local_path):
#     for file in files:
#         file_s3 = os.path.normpath(path + '/' + file)
#         file_local = os.path.join(path, file)
#         print("Upload:", file_local, "to target:", file_s3, end="")
#         client.upload_file(file_local, bucketname, file_s3)
#         print(" ...Success")

import boto3
import os

# Initialize the S3 client
client = boto3.client('s3')

# Define the local folder and S3 bucket
local_path = "C:/Users/parth/Downloads/test"  # Change this to your actual folder
bucket_name = "pmalladi-program3"

# Extract only the folder name (e.g., "test")
base_folder_name = os.path.basename(local_path)

# Upload files while keeping the folder structure under "test/" in S3
for path, _, files in os.walk(local_path):
    for file in files:
        file_local = os.path.join(path, file)
        
        # Get relative path and prepend base_folder_name
        relative_path = os.path.relpath(file_local, local_path)  # Get path relative to "test"
        file_s3 = os.path.join(base_folder_name, relative_path).replace("\\", "/")  # Ensure forward slashes

        print(f"Uploading {file_local} to s3://{bucket_name}/{file_s3} ...", end=" ")
        
        # Upload file to S3
        client.upload_file(file_local, bucket_name, file_s3)
        
        print("Success")

print("Upload complete!")
