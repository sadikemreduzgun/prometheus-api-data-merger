# Get Node Exporter and Libvirt Exporter metrics using Prometheus API

## A Quick Explanation:
#### In data folder there is all_queries csv file. It contains node exporter and libvirt exporter queries.
#### In src file there are codes. In python file, organzier.py there are functions to organize urls, instances, queries.

⚙️ curly_organizer function deletes statements in selector: "{}",and time selector: "[]". curly_organizer puts selected instance, time selector, device name.

⚙️ organize_url function is used to some problems at query and prevent the mess of characters like " + ", " " ", " * ". Because generally operations like addition on query can't be done. 

⚙️ organize_instance function is used to give instance and device name to organize_url function.

⚙️ reach_selection_data.py file is used to return instance and device name by getting default date and time from reach_time.py file's give_default_dates function. That fundtion recursively finds a common date and time of the virtual machine(s) and server. Default time interval between start and end time is 1 day and 5 minutes it is changeable.

⚙️ main.py uses mentioned-above functions. It creates dataframes by performing some operations(explained in code) and saves them.

## Required Packages ❗
'''pip
pip install requests==2.25.1
pip install pandas==1.5.3
pip install numpy==1.24.2
'''
built-in packages like: datetime, json


## To Run
👓 Just run main.py Python file after getting required packages downloaded. If everything goes correctly, you will see 2 csv files which contain metrics data in the folder named as "out". If some error occurs, error will be printed. 

##### DO NOT HESITATE WRITING ME WHEN A PROBLEM OCCURED: sed3718@gmail.com
