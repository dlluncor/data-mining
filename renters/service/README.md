Set Up Python Env
1. pip install -r requirements.txt

Set Up MongoDB
1. Download mongo db from official web site
2. mongod --dbpath=data_store_folder_path

Run Service
1. python app.py

Notice: you have to start mongo db before you start service.

---------------
# Set Up Prod Instance on AWS

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

4. Download Application Codes
    The application locates at /u/app on the server.

    ```
    sudo mkdir -p /u/app
    sudo git clone https://github.com/bonjoylabs/data-mining.git
    ```
5. Start Server
    ```
    nohup APP_ENV=PROD python app.py > run.log 2 > &1 &
    ```
