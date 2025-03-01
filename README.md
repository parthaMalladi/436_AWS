# 436_AWS

## This program is run entirely through the terminal. The two possible commands are "restore" and "backup"

**To execute restore**: py program3.py restore &lt;AWS-bucket-name::directory-name&gt; &lt;local-directory-name&gt;

**To execute backup**: py program3.py backup &lt;local-directory-name&gt; &lt;AWS-bucket-name::directory-name&gt;
- local directory file path can be simply copied from file explorer but has to have any backward slashes replaced with forward slashes.
    - get full filepath from root of the computer such as C: disk
    - replacing the backward slashes must be done manually by the user
- AWS bucket name is the name the user gives to their S3 bucket.
    - bucket name must be unique, otherwise an error will be thrown
    - if the bucket does not exist, if the name is valid, the bucket will be automatically created
    - after the bucket name, please input "::" and any folder path
- AWS directory-name is the path in the S3 bucket.
    - after the "::", leave empty to just copy the contents of the local folder into the bucket
    - specifying a directory path will insert the local files at the directory path location
    - if the directory path does not exist, it will be automatically created