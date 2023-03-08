from datetime import datetime, timedelta
import json
import requests as rq


def give_default_dates(day_back=0, hour_back=3, min_back=30):

    # get date one day ago   
    end_time = datetime.now() - timedelta(days=day_back, hours=1)
    # stop the change of number of metrics in the loop in main.py, get stable time because it always is changing  
    end_time -= timedelta(seconds=end_time.second, microseconds=end_time.microsecond)
    
    # get date 1 day and 5 mins. ago
    start_time = (datetime.now() - timedelta(days=day_back, hours=hour_back, minutes=min_back))
    # stop the change of number of metrics in the loop in main.py, get stable time because it always is changing    
    start_time -= timedelta(seconds=start_time.second, microseconds=start_time.microsecond)

    # turn date into string
    end = str(end_time.date())
    # turn date into the format which is used on url
    end = end + "T"
    end = end + str(end_time.time())[0:12] + "Z"

    # turn end date into string
    start = str(start_time.date())
    # turn end date into the format which is used on url
    start = start + "T"
    start = start + str(start_time.time())[0:12] + "Z"

    query = "libvirt_domain_block_stats_allocation"
    url_lib = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=3m"
    query="node_load1"
    url_node = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=3m"

    # get data using api
    data_node = rq.get(url_node)
    # turn data into a dictionary
    data_node = data_node.json()
    # get data using api
    data_lib = rq.get(url_lib)
    # turn data into a dictionary
    data_lib = data_lib.json()
    print(len(data_node['data']['result']))
    
    #print(data_lib['data']['result'][0]['values'])
    # find a date which gives data recursively 
    if len(data_node['data']['result']) == 0 or len(data_lib['data']['result']) == 0:
        print("no data")
        return give_default_dates(days=day_back+1)
    # return processed dates
    return start, end


# 2023-02-21T10:59:25.479Z
# Output: The current date and time is 2022-03-19 10:05:39.482383
#give_default_dates()
