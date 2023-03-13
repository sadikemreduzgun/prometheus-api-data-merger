# Get Node Exporter and Libvirt Exporter metrics using Prometheus API

## A Quick Explanation:
#### In data folder there is all_queries csv file. It contains node exporter and libvirt exporter queries.
#### In src file there are codes. In python file, organzier.py there are functions to organize urls, instances, queries.

⚙️ In organize.py file there are 3 organizer function: curly_organizer function deletes statements in selector: "{ }",and time selector: "[ ]". curly_organizer puts selected instance, time selector, device name.

⚙️ organize_url function is used to some problems at query and prevent the mess of characters like " + ", " " ", " * ". Because generally operations like addition on query can't be done. 

⚙️ organize_instance function is used to give instance and device name to organize_url function.

⚙️ reach_selection_data.py file is used to return instance and device name by getting default date and time from reach_time.py file's give_default_dates function. That fundtion recursively finds a common date and time of the virtual machine(s) and server. Default time interval between start and end time is 1 day and 5 minutes it is changeable.

⚙️ main.py uses mentioned-above functions. It creates dataframes by performing some operations(explained in code) and saves them.

## Required Packages ❗
```
certifi==2022.12.7
charset-normalizer==3.0.1
idna==3.4
numpy==1.24.2
pandas==1.5.3
python-dateutil==2.8.2
pytz==2022.7.1
requests==2.28.2
six==1.16.0
urllib3==1.26.14
```
### to install:
```pip
pip install -r requirements.txt
```

## To Run
👓 Just run main.py Python file after getting required packages downloaded. If everything goes correctly, you will see 2 csv files which contain metrics data in the folder named as "out". If some error occurs, error will be written in var/log.txt. 

##### DO NOT HESITATE WRITING ME WHEN A PROBLEM OCCURED: sed3718@gmail.com
