import os
import sys
import boto3

def createBucket(bucketName):
    s3 = boto3.client("s3")

    for bucket in s3.list_buckets()["Buckets"]:
        if bucket["Name"] == bucketName:
            print("bucket " + bucketName + " exists")
            return

    s3.create_bucket(Bucket=bucketName)
    print(bucketName + " created")

# def backup(localPath, awsPath):
#     # create/check for S3 bucket
#     bucketName = awsPath.split("::")[0]
#     createBucket(bucketName)

#     baseFolder = awsPath.split("::")[1]
#     if (baseFolder == ""):
#         baseFolder = os.path.basename(localPath)
    
#     print("baseFolder: " + baseFolder)

#     client = boto3.client("s3")

#     for path, dir, files in os.walk(localPath):
#         for file in files:
#             localFile = os.path.join(path, file)
#             relativePath = os.path.relpath(localFile, localPath)
#             s3File = os.path.join(baseFolder, relativePath)
#             client.upload_file(localFile, bucketName, s3File)
    
#     print("backup complete")

def backup(localPath, awsPath):
    """Uploads localPath contents into the correct S3 structure based on awsPath."""
    # Extract bucket name and folder path
    parts = awsPath.split("::")
    bucketName = parts[0]
    
    # Ensure the bucket exists
    createBucket(bucketName)

    # Determine the base S3 folder
    baseFolder = parts[1] if len(parts) > 1 and parts[1] else os.path.basename(localPath)

    # Ensure that the local folder name (e.g., "test") is included in the structure
    localFolderName = os.path.basename(localPath)
    fullS3Path = os.path.join(baseFolder, localFolderName).replace("\\", "/")  # Ensures "lmao/test/"

    print(f"Uploading to S3 bucket: {bucketName}, inside folder: {fullS3Path}")

    client = boto3.client("s3")

    # Walk through local directory and upload
    for path, _, files in os.walk(localPath):
        for file in files:
            localFile = os.path.join(path, file)
            relativePath = os.path.relpath(localFile, localPath)
            
            # Ensure proper folder structure inside S3
            s3File = os.path.join(fullS3Path, relativePath).replace("\\", "/")  # Enforce "lmao/test/..."

            print(f"Uploading {localFile} to s3://{bucketName}/{s3File} ...")
            client.upload_file(localFile, bucketName, s3File)
    
    print("Backup complete.")

def restore(localPath, awsPath):
    # create/check for S3 bucket
    bucketName = awsPath.split("::")[0]
    createBucket(bucketName)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:")
        print("py program3.py restore <AWS bucket-name::directory-name> <local directory name>")
        print("or")
        print("py program3.py backup <local directory name> <AWS bucket-name::directory-name>")
        sys.exit(1)
    
    action = sys.argv[1]
    localPath = ""
    awsPath = ""

    if action == "backup":
        localPath = sys.argv[2]
        awsPath = sys.argv[3]
        backup(localPath, awsPath)
    elif action == "restore":
        localPath = sys.argv[3]
        awsPath = sys.argv[2]
        restore(localPath, awsPath)
    else:
        print("action: " + action + ", does not exist")
        sys.exit(1)