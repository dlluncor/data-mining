# How to Script Data from Farmers

## Related Files:
```
.
├── browser_robot.rb
├── data
│   └── dataset
└── misc
    ├── Xwrapper.config
    ├── locale
    └── scripting.py
```

* browser_robot.rb is a ruby file to scripting data from website using watir-webdriver
* data/dataset is the folder to store original dataset and results
* misc folder contains files for scripting and setup machines.

## Preparation

### Create AWS instance
Please use Chris' account to login https://aws.amazon.com
You could create instance from scratch or use pre-defined image.

* Pre-defined image
    It's name is browser_robot and it is out-of-the-box, you don't have to config it.

* New Instance
    If you want to create a new instance, you have to set up the environment to run the script.

### Set Up Environment for New Instance
```
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install build-essential
sudo apt-get install ruby ruby-dev unzip git

# Install X server
# Chrome require X server to run
sudo apt-get install xorg

# Install Google chrome
$ wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
$ sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
$ sudo apt-get update
$ sudo apt-get install google-chrome-stable

# Install ruby gem
sudo gem install watir-webdriver

# Install chromedriver
#http://chromedriver.storage.googleapis.com/index.html
wget http://chromedriver.storage.googleapis.com/2.18/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
```

### Update Configurations to Run Scripting
Once you have create instances to run scripting program. You need add the machine information to machines dict in misc/scripting.py.
And also update the dataset configurations to make sure correct values are set. You can feel free to set the tag to as value your want.

You could also set `filename` and `tag` for each machine in machines dict, which will overwrite the value of dataset.


### Start Script
```
cd ~/data-mining/renters/price-engine
```
#### Init Machines
Run below command to init machines to run script.
```
python misc/status_check.py -i all -a init
```
Task the command will do:
1. Upload files required to run Chrome without GUI environment.
2. Split the data set file into several files, same count as machines.
3. Checkout out latest codes to home folder.

#### Start Script
```
python misc/status_check.py -i all -a start
```

#### Check the Running Status of the Script on Remote Machine
```
python misc/status_check.py -i all -a check
```

or

```
# Auto run the check command every 5min
python misc/scripting.py -i all -a check -l forever
```

Notice: once the check command detect the script is started (by file lock),
not finished and not running, it will trying to resume the task. So use loop
forever is a good practice if you want to keep the scripting running.

#### Handle Fail Samples
Sometimes the script will fail to collect data for some samples. The failed
samples are stored in {dataset_path}/error_{tag}_{id}.json. When the first round of scripting is finished, you could to run the failed samples on remote machine to collect as many samples as possible. What you need to do is:
1. Go to misc/scripting.py
2. Edit the machines dict, change value of filename key of the specific machine that finished the first round script to the name of the error file, and also set a new tag value.
3. Run start command for the specific machine
```
python misc/status_check.py -i 0 -a start
```

#### Pull The Result Files
When the script is finished run below command to download all the results files to dataset folder on local machine.
```
python misc/scripting.py -i all -a pull -t no_crosses,missed
```

## Merge Result files
After all the samples are scripted successfully, next thing need to do is merge the result. Use below command:

```
python misc/scripting.py -i all -a merge -t no_crosses,missed,complement
```

and you will get a 'final_result.csv' under the data set folder.
