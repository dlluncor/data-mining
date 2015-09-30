# Develop Env on Mac

## Setup Python ENV
1. pip install -r requirements.txt

## Set Up MongoDB
1. Download mongo db from official web site
2. `mongod --dbpath=data_store_folder_path`


## Run Service

### Run service under debug mode
```
python app.py
```

### Run service under prod mode
```
sudo APP_ENV=PROD python app.py
```

Notice: you have to start mongo db before you start service.

---------------
# Set Up Prod Instance on AWS (Ubuntu 14.04)

## Create EC2 Instance
1. Open the 80 port in the Security Groups
2. Create new Key Pair if necessary

## Upgrade the Instance
1. Execute below commands to upgrade instance once the instance is created.
    ```
    sudo apt-get update
    sudo apt-get upgrade
    ```
2. Set Up Python Dev Env with the following commands
    ```
    sudo apt-get install -y git
    sudo apt-get install python-dev
    sudo apt-get install python-pip
    sudo pip install flask
    sudo pip install mongoengine
    ```

    Tips:
    1. If get below error when installing gevent, try command: `CFLAGS='-std=c99' pip install gevent`
    Ref: http://stackoverflow.com/questions/32417141/cant-install-gevent-osx-10-11
    ```
    In file included from gevent/libev.h:2:
    libev/ev.c:483:48: warning: '/*' within block comment [-Wcomment]
    /*#define MIN_INTERVAL  0.00000095367431640625 /* 1/2**20, good till 2200 */
    ```

3. Install Mongodb
    ```
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
    echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org
    ```

4. Update locale to run mongo locally
Change content of /etc/default/locale:
```
LANG="en_US.UTF-8"
LANGUAGE="en_US:en"
LC_ALL="en_US.UTF-8"
```

5. Secure MongoDB
After install mongodb, need to enable access control and create specific user to access credit card information.
```
mkdir -p /private/var
cd /private/var
sudo openssl rand -base64 741 > mongodb-keyfile
sudo chmod 600 mongo-private-key.pem
sudo chown mongodb:mongodb mongo-private-key.pem
```

Edit /etc/mongo.conf. Enable/add below line:
```
keyFile=/private/var/mongo_private_key.pem
```

Restart mongodb

Create Users
Create admin user
```
$ mongo
> use admin
db.createUser(
    {
      user: "admin",
      pwd: "xxxx",
      roles: [ "root" ]
    }
)
```
Create new user for credit card db
```
$ mongo 127.0.0.1/admin -u admin -p
> use credit_cards
> db.createUser(
    {
      user: "ccwriter",
      pwd: "xxxx",
      roles: [
         { role: "readWrite", db: "credit_cards" }
      ]
    }
)
```

Access Database:
```
mongo 127.0.0.1/credit_cards -u ccwriter -p
```
Default passwd is zhen passwd need to change later
Ref:
1. http://docs.mongodb.org/manual/tutorial/generate-key-file/
2. http://docs.mongodb.org/manual/tutorial/enable-authentication/
3. http://docs.mongodb.org/manual/tutorial/manage-users-and-roles/
4. http://docs.mongodb.org/manual/reference/connection-string/

5. Download Application Codes
    The application locates at /u/app on the server.

    ```
    sudo mkdir -p /u/app
    sudo chmod -R 777 /u/app
    sudo git clone https://github.com/bonjoylabs/data-mining.git
    ```
6. Start Server
    ```
    sudo APP_ENV=PROD nohup python app.py >> run.log 2>&1 &
    ```

7. Config Upstart to make service start when machine start by create a new files /etc/init/payment-service.conf with below content:

    ```
    description "Flask Application for Renters Insurance Portal"

    start on runlevel [2345]
    stop on runlevel [!2345]

    respawn

    chdir /u/app/data-mining/renters/payment_service
    exec sudo APP_ENV=PROD MONGODB_URI=mongodb://ccwriter:[password]@127.0.0.1:27017/credit_cards python app.py >> /var/log/payment-service.log
    ```

    manually start the service:
    ```
    sudo start renters
    ```

    manually start the service:
    ```
    sudo stop renters
    ```

    check logs
    ```
    tail -f /var/log/upstart/payment-service.log
    ```
