# 436_AWS

## Setup AWS credentials and login by running "AWS Configure" before executing the program. Screenshots and Design is documented in the Word Doc named "Documentation.docx"

## This program is run entirely through the terminal. The two possible commands are "restore" and "backup"

**To execute restore**: py program3.py restore &lt;AWS-bucket-name::directory-name&gt; &lt;local-directory-name&gt;
- **local-directory-name** is the directory path copied from file explorer but has to have any backward slashes replaced with forward slashes.
    - get full directory path from root of the computer such as the C: disk
    - replace any backward slashes with forward slashes manually
    - the final directory name is the location the AWS folder will be restored to
    - if the folder name does not exist, then it will be created at the given location
- **AWS-bucket-name** is the name the user gives to their S3 bucket.
    - restore will not work if the bucket does not exist
    - after the bucket name, please input "::" and any directory path
- **directory-name** is the path in the S3 bucket.
    - after the "::", leave empty to restore all the contents of the S3 bucket to the local directory
    - if a directory path is included, the program will copy only the contents of the last folder named in the directory path
- **Example:** py program3.py restore partha-program-css436:: C:/Users/parth/Downloads
    - access the bucket named "partha-program-css436". Since nothing is specified after "::", copies all the contents of the bucket to the local location "C:/Users/parth/Downloads"
    - if after the "::", a path was specified such as "partha-program-css436::Folder/SubFolder", then the contents in "SubFolder" will be copied to the local location "C:/Users/parth/Downloads"
    - if a local folder does not exist, adding it to the end of the local location with create that folder and copy the contents of the bucket. For instance ""C:/Users/parth/Downloads/storage" would create a new folder called "storage" in downloads and then copy all of the contents of the S3 bucket "partha-program-css436"

**To execute backup**: py program3.py backup &lt;local-directory-name&gt; &lt;AWS-bucket-name::directory-name&gt;
- **local-directory-name** is the directory path copied from file explorer but has to have any backward slashes replaced with forward slashes.
    - get full directory path from root of the computer such as the C: disk
    - replacing the backward slashes must be done manually by the user
- **AWS-bucket-name** is the name the user gives to their S3 bucket.
    - bucket name must be unique, otherwise an error will be thrown
    - if the bucket does not exist, if the name is valid, the bucket will be automatically created
    - after the bucket name, please input "::" and any directory path
- **directory-name** is the path in the S3 bucket.
    - after the "::", leave empty to just copy the contents of the local folder into the bucket
    - specifying a directory path will insert the local files at the directory path location
    - if the directory path does not exist, it will be automatically created in the S3 bucket
- **Example:** py program3.py backup C:/Users/parth/Downloads/Folder partha-program-css436::
    - copies all the contents from the folder titled "Folder", including the folder itself
    - copies to the bucket titled "partha-program-css436"
    - changing "partha-program-css436::" to "partha-program-css436::storage" would create a folder called "storage" in AWS and then copy "Folder" and all its contents