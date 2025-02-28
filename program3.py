import boto3
import os
import sys

# Create an S3 client
s3 = boto3.client("s3")

# Get a list of all buckets
response = s3.list_buckets()

# Print bucket names
print("S3 Buckets in your AWS account:")
for bucket in response['Buckets']:
    print(f"- {bucket['Name']}")

file_path = 'C:/Users/parth/Downloads/test/kekw.txt'
bucket_name = 'pmalladi-program3'

s3.upload_file(file_path, bucket_name, 'yikes')