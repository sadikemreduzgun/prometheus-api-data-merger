from organizer import *
import pandas as pd
import requests as rq
import numpy as np


df = pd.read_csv('queries.csv')
start = "2023-02-21T10:59:25.479Z"
end = "2023-02-21T19:59:25.479Z"
step = "5s"
boole = True
devices = reach_device()
save = 0
saves = 0
print(devices)
temp_data = 0
count = -4
titles = ['time_stamp']
hold_query = df.iloc[0,1]
mets= 0
lastk = 12
boole_node = True
sws = 0

for query in df.iloc[:,1]:
    boole2=True
    boole3 = True

    hold_if = False
    check, instance = organize_instance(query)
    #hold_query = query
    if check == "libvirt":
        in_count = 1
        for device in devices:
            temp, instance = organize_instance(query, device)
            metrics = curly_organizer(query, instance, step)
            metrics = organize_url(metrics, start, end)
            hold = metrics
            metrics = rq.get(metrics)
            metrics = metrics.json()
            hold = count
            
            if_same = (hold_query == query)
            
            print(if_same)
            temp_data, count, boole, mets, boole2, boole3,save,saves = organize_dataframe(metrics,count ,boole, temp_data, if_same,boole2, len(devices),in_count, mets, boole3,save,saves)
            print(hold,count)
            if hold != count:
                try:
                    titles.append(device +" : " + df.iloc[count,0])
                except:
                    print("whooooa!")
            in_count += 1

        
    if check =="node":
        temp, instance = organize_instance(query)
        metrics = curly_organizer(query, instance, step)
        metrics = organize_url(metrics, start, end)
        hold = metrics
        metrics = rq.get(metrics)
        metrics = metrics.json()

        sws, boole_node = organize_node_df(metrics, boole_node, sws)

        print(hold,count)
        if hold != count:
            try:
                titles.append(device +" : " + df.iloc[count,0])
            except:
                print("whooooa!")
    
    hold_query = query


# start title list with one title which is the same for all
# a function to convert byte into megabyte
def div(x):
    x = x/1048576
    y="{:.3f}".format(x)
    y=y+"Mb"
    return y

# get data into dataframe object
dataframe = pd.DataFrame(save)

dataframe.to_csv('last_state.csv')
