from organizer import *
import pandas as pd
import requests as rq
import numpy as np
from datetime import date
from reach_time import *


# read csv which contains queries
df = pd.read_csv('../data/all_queries.csv')
store_lib = []
store_node = []
q_name = []
# get default-recent time data

#start = "2023-02-21T10:59:25.479Z"
#end = "2023-02-21T19:59:25.479Z"
#start = "2023-02-27T06:22:25.479Z"
#end= "2023-02-28T07:39:25.479Z"
start, end = give_default_dates(day_back=0,hour_back=1,min_back=30)
queries = []
# define default step and query function step
step = "20s"
step_func = "5s"
# define a boolean to be used to run a statement for once
one_crap_boolean = True
# get Virtual machine names 
devices = reach_device(start,end)
# a weird boolean too, to execute a statement once
two_crap_boolean = True
# define a list to store query names which returns no data and save them in var/log.txt
non_saved_log = []
# define lists for to store column names
titles = ["time_stamp"]
titles_node = ["time_stamp"]
titles_node_less = []
title_count_lib=0
# read queries, organize them and gather their values
#df.iloc[:, 2], df.iloc[:, 1]
handling_bool = True

for name, col in df.iterrows():
    
    query_name = col["query_name"]    
    query = col["query"]
    q_name.append(query_name)

    # booleans to execute a statement for each loop turn
    three_crap_boolean = True
    four_crap_boolean = True

    # get checking data
    check, instance = organize_instance(query)

    # go depending on data
    if check == "libvirt":
        # a counter of device loop
        in_count = 1
        # processes of devices taken by a function
        for device in devices:
            # get instance to run curly organizer function
            temp, instance = organize_instance(query, device)
            # run curly organizer delete instance and replace it
            url = curly_organizer(query, instance, step_func)
            # get data after organizing the url
            url = organize_url(url, start, end,step)
            store_lib.append(url)
            # get data using requests modul
            metrics = rq.get(url)


    # go depending on data
    if check == "node":
        # get instance to run curly organizer function
        temp, instance = organize_instance(query)
        # run curly organizer delete instance and replace it
        url = curly_organizer(query, instance, step_func)
        # get data after organizing the url
        url = organize_url(url, start, end, step)
        # hold URL to be used later
        hold = url
        # get data using requests modul
        store_node.append(url)


all = [q_name, store_node, store_lib]
pd.DataFrame(all)
print(pd)
