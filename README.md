# Photo App

This application enables users to upload and view uploaded pictures.

## Getting Started

Download the repository or use git clone to get a copy of the project on your system.
```
git clone https://github.com/shivani-nadkarni/photo_app.git
```
### Prerequisites

Run reqirements.txt to install python libraries.
```
pip install -r requirements.txt
```
Install postgreSQL.
```
apt-get install postgresql
```
In the postgres console, create a database and name it 'photo_app'.

Change the database URL accordingly. For postgreSQL, we have default user as 'postgres' and no default password. You can set password for the same. I have set 'postgres' as the password. 

You can then set environment variables for database URL and secret key as follows.
```
export DATABASE_URL="postgresql://postgres:postgres@localhost/photo_app"
export SECRET_KEY='1234sasdf//;;'
``` 
To create the database, open python interpretor.
```
python3
```
Then type the following the create the database.
```
from photo_app.routes import database
from photo_app.db import User, Photo, create_db

create_db()
```
Now, we create a minio object storage server, where we will be uploading images. Also, download the minio client(mc) command.
```
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio

wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
```
Type the following to create a shortname 'myminio' to the cloud storage service. I have used the default credentials for the service. You are free to set your own and insert them accordingly in the below command.
```
mc alias set ALIAS <YOUR-S3-ENDPOINT> <YOUR-ACCESS-KEY> <YOUR-SECRET-KEY> 

mc alias set myminio http://192.168.1.107:9000 minioadmin minioadmin
```
We will then need to create a bucket and set download permission for it.
```
mc cb myminio/mytestbucket
mc set download myminio/mytestbucket/
```
Now export the following variables.
```
export S3_URL='http://192.168.1.107:9000'
export S3_KEY='minioadmin'
export S3_SECRET='minioadmin'
export S3_BUCKET='mytestbucket'
```
Now we are good to run the application.

## Run

To start minio server, type the following.
```
minio server data 
```
To start flask server, run the following command in the base folder.
```
python3 -m photo_app
```
Open the flask URL in the browser.

### Demo

You can sign in the portal by using the credentials username as 'guest' and password 'guest'.

Once logged in, upload pictures by browsing picture of you choice and then click on upload.
All uploaded pictures can be viewed through the thumbnails or by clicking the image links.

Once done, you can logout of the portal by clicking 'Logout' on the top right corner. 

## Authors

Shivani Nadkarni - https://github.com/shivani-nadkarni


## Acknowledgments

Thanks to my brother and mentor viren-nadkarni for guiding and inspiring me to build this - https://github.com/viren-nadkarni
