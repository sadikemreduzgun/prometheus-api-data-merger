# Get Node Exporter and Libvirt Exporter metrics using Prometheus API

## A Quick Explanation:
#### In /src there is nodes2.csv file, it contains node exporter and other exporters' queries.
#### In /src file there are codes. In python file, organzier.py there are functions to organize urls, instances, queries. Merge_processes.py is for merging queries, main.py is starting merging by organizing time.

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

## To Install:
```pip
pip install -r requirements.txt
```

## To Run
👓 Just run main.py Python file after getting required packages downloaded. You will have as many files as the number of instances which are node exporter downloaded.  

##### DO NOT HESITATE WRITING TO ME WHEN A PROBLEM OCCURED: sed3718@gmail.com
