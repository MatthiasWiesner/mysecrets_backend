# MySecrets Backend

Webserver to store and deliver client encrypted content.

Using:
- Flask
- Orator
- Postgresql

## Installation
Create database and user in postgresql
```
create database mysecrets;
create user mysecret with encrypted password '<very-secret-passwd>';
grant all privileges on database mysecrets to mysecret;
```

Install mysecrets-backend as mysecrets user

pipenv needs to be installed, necessary libs as well
```
su mysecrets -c '/usr/local/bin/pipenv install'
su mysecrets -c '/usr/local/bin/pipenv shell'

# within pipenv shell
python db.py migrate
python db.py db:seed

cp ./resources/mysecrets-backend.service /etc/systemd/system/mysecrets-backend.service
chown -R mysecrets: .
systemctl daemon reload
systemctl enable mysecrets-backend.service
systemctl start mysecrets-backend.service
```