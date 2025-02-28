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

###############################################################################################################################

# Initialize S3 client
s3 = boto3.client('s3')

# Define bucket and folder to download
bucket_name = "pmalladi-program3"
s3_folder = "test/"  # S3 folder prefix (must end with '/')

# Define local path to save files
local_path = "C:/Users/parth/Downloads/store"  # Change this to your desired local folder

# Ensure local path exists
if not os.path.exists(local_path):
    os.makedirs(local_path)

# List objects in the specified S3 folder
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_folder)

if 'Contents' in response:
    for obj in response['Contents']:
        s3_key = obj['Key']  # Full S3 key (including path)
        
        # Remove the base folder prefix to get the relative path
        relative_path = os.path.relpath(s3_key, s3_folder)

        # Construct full local path
        local_file_path = os.path.join(local_path, relative_path)
        local_file_path = local_file_path.replace("/", os.sep)  # Ensure correct path separator

        # Create local directories if they don’t exist
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        print(f"Downloading {s3_key} to {local_file_path} ...", end=" ")

        # Download the file
        s3.download_file(bucket_name, s3_key, local_file_path)

        print("Success")

    print("Download complete!")
else:
    print(f"No files found in s3://{bucket_name}/{s3_folder}")
