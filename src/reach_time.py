from datetime import datetime, timedelta
import json
import requests as rq


def give_default_dates(days=1):
    # get date one day ago
    currentDateAndTime = datetime.now() - timedelta(days)
    # get date 1 day and 5 mins. ago
    current_minus_5_min = (datetime.now() - timedelta(days+1,minutes=5))

    # turn date into string
    end = str(currentDateAndTime.date())
    # turn date into the format which is used on url
    end = end + "T"
    end = end + str(currentDateAndTime.time())[0:12] + "Z"

    # turn end date into string
    start = str(current_minus_5_min.date())
    # turn end date into the format which is used on url
    start = start + "T"
    start = start + str(current_minus_5_min.time())[0:12] + "Z"

    query = "libvirt_domain_block_stats_allocation"
    url_lib = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=3m"
    query = "node_load1"
    url_node = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=30s"

    # get data using api
    data_node = rq.get(url_node)
    # turn data into a dictionary
    data_node = data_node.json()
    # get data using api
    data_lib = rq.get(url_lib)
    # turn data into a dictionary
    data_lib = data_lib.json()

    # find a date which gives data recursively 
    if len(data_node['data']['result']) == 0 or len(data_lib['data']['result']) == 0:

        return give_default_dates(days=days+1)
    # return processed dates             
    return start, end


# 2023-02-21T10:59:25.479Z
# Output: The current date and time is 2022-03-19 10:05:39.482383
