import os
import sys
import boto3

# helper function to check or create a bucket
def createBucket(bucketName, action):
    s3 = boto3.client("s3")

    # check if bucket already exists and return true if it does
    for bucket in s3.list_buckets()["Buckets"]:
        if bucket["Name"] == bucketName:
            print("bucket " + bucketName + " exists")
            return True

    # return false if bucket doesnt exist
    if (action != "backup"):
        return False
    
    # create bucket if it doesnt exist
    s3.create_bucket(Bucket=bucketName)
    print(bucketName + " created")

# function to backup to AWS
def backup(localPath, awsPath):
    # extract bucket name and file path
    bucketName = awsPath.split("::")[0]
    basePath = awsPath.split("::")[1]

    # check for bucket existence
    createBucket(bucketName, "backup")

    # extract local folder name
    localFolderName = os.path.basename(localPath)

    # create full S3 path
    s3Path = os.path.join(basePath, localFolderName) 

    # upload local folder contents
    client = boto3.client("s3")

    for path, dir, files, in os.walk(localPath):
        for file in files:
            localFile = os.path.join(path, file)
            relativePath = os.path.relpath(localFile, localPath)
            s3File = os.path.join(s3Path, relativePath).replace("\\", "/")

            # upload to S3 bucket
            client.upload_file(localFile, bucketName, s3File)
            print(f"Backing up {localFile.replace("\\", "/")} to {bucketName}::{s3File}")
    
    print("BACKUP COMPLETE")

# function to restore from AWS
def restore(localPath, awsPath):
    # extract bucket name and file path
    bucketName = awsPath.split("::")[0]
    basePath = awsPath.split("::")[1]

    # add / to traverse folders
    if len(basePath) > 1:
        basePath = basePath + "/"

    # check for bucket existence
    if not createBucket(bucketName, "restore"):
        print("bucket called " + bucketName + " does not exist")
        return
    
    # make local path if it doesnt exist
    if not os.path.exists(localPath):
        os.makedirs(localPath)    

    # check for folder in S3 bucket
    client = boto3.client("s3")
    response = client.list_objects_v2(Bucket=bucketName, Prefix=basePath)

    # get S3 objects
    if "Contents" in response:
        for cont in response["Contents"]:
            key = cont["Key"]
            relativePath = os.path.relpath(key, basePath)

            # create local path
            localFilePath = os.path.join(localPath, relativePath)
            os.makedirs(os.path.dirname(localFilePath), exist_ok=True)

            # restore from S3 bucket
            client.download_file(bucketName, key, localFilePath)
            print(f"Restoring from {bucketName}::{key} to {localFilePath.replace("\\", "/")}")
    else:
        print("S3 Bucket path does not exist")
        return

    print("RESTORE COMPLETE")

# main function
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:")
        print("py program3.py restore <AWS-bucket-name::directory-name> <local-directory-name>")
        print("or")
        print("py program3.py backup <local-directory-name> <AWS-bucket-name::directory-name>")
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