# Photo App
This application enables users to upload and view uploaded pictures. The application will run on Heroku with postgresql database attached to it. The uploaded images are stored on AWS S3.

## Getting Started
Download the repository or use git clone to get a copy of the project on your system.
```
$ git clone https://github.com/shivani-nadkarni/photo_app.git
```
### Prerequisites
Run reqirements.txt to install python libraries.
```
$ pip install -r requirements.txt
```
### PostgreSQL Installation
I will first create postgreSQL database locally and later push it to heroku.

In order to do that let's install postgreSQL on our system.
```
$ sudo apt-get install postgresql
```
PostgreSQL comes with the default role 'postgres'. In order to proceed, I created a role with name same as my system root username. You can do the same as follows.
```
$ sudo -u postgres
postgres@vostro:~$ createuser --interactive
Enter name of role to add: shivani
Shall the new role be a superuser? (y/n) y
postgres@vostro:~$ \q
```
Exit the postgres console.

### Database Intialisation
In the postgres console on our system, create a new database and name it 'photo_app'.
 
To initialise our database, open python interpretor.
```
$ python3
```
Then type the following the create the database.
```
>> from photo_app import database
>> from photo_app.models import User, Photo, create_db
>> create_db()
```
### Setting-up Heroku with PostgreSQL
Inorder to use Heroku CLI, we will have to install heroku on our system and then login into your heroku account.
```
$ sudo snap install heroku --classic
$ heroku login
```
Once your login is verified on the browser, next we create a new app on heroku, which is going to receive the cloned source code. Leave the name blank and heroku will generate a default name for your app. I have named the app 'photoapp-shiv'.
```
$ heroku create photoapp-shiv
``` 
Note down the app URL, we will later use it to open the app in the browser.

Furthermore, we will also use heroku-postgres for deploying the database in the same heroku app.
```
heroku addons:create heroku-postgresql:hobby-dev
```
### Pushing the database
The following command pushes local database to the heroku app's primary database.
```
$ heroku pg:push photo_app HEROKU_POSTGRESQL_SILVER --app photoapp-shiv
```
You can access the heroku database from your system. The following commands gives the database information and opens postgresql console respectively.
```
$ heroku pg:info
$ heroku pg:psql
```
### Set-up S3 for Image Storage
Open a new account on Amazon AWS. Create an IAM user for safety. Obtain the credentials for Access-key and Secret-key. We shall use this for establishing connection.
### Config variables
Next, set environment variables necessary to run your application on heroku.
```
$ heroku config:set VAR_NAME1=VAR_VALUE1 VAR_NAME2=VAR_VALUE2
```
Following are the names of the variables to be configured. Enter the key names as they are. And the values should be as per your application set-up.

1. SECRET_KEY: <YOUR_APPLICATION_SECRET KEY>
2. S3_BUCKET:  <YOUR_S3_BUCKET_NAME>
3. S3_KEY:     <YOUR_S3_KEY>
4. S3_SECRET:  <YOUR_S3_SECRET>

Heroku will set a database URL for the database on it's own. You can view it through following.
```
$ heroku config:get DATABASE_URL
```
### Deployment on Heroku
Now we will push the local code to the heroku app.
```
$ git add -A
$ git commit -m "Heroku Demo."
$ git push heroku master
```
## Run
Click on the URL generated on the console (When we created the app, the url is given), to view the app on the browser. Or type the following.
```
$ heroku open
```
You can also test your application locally. For that you will have to just add .env file containing the environment variables (config variables) to your base folder. Use the following to do that. 
```
$ heroku config:get <VAR-NAME> >> .env
$ heroku local
```
### Demo
You can sign in the portal by using the credentials username as 'guest' and password 'guest'.

Once logged in, upload pictures by browsing picture of you choice and then click on upload.
All uploaded pictures can be viewed through the thumbnails or by clicking the image links.

Once done, you can logout of the portal by clicking 'Logout' on the top right corner. 
## Author
Shivani Nadkarni - https://github.com/shivani-nadkarni
## Acknowledgments
Thanks to my brother and mentor viren-nadkarni for guiding and inspiring me to build this - https://github.com/viren-nadkarni
