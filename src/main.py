from organizer import *
import pandas as pd
import requests as rq
import numpy as np


df = pd.read_csv('../data/all_queries.csv')
start = "2023-02-21T10:59:25.479Z"
end = "2023-02-21T19:59:25.479Z"
step = "5s"
boole = True
devices = reach_device()
save = 0
saves = 0
boole6=True
print(devices)
temp_data = 0
count = -4
hold_query = df.iloc[0,1]
mets= 0
lastk = 12
boole_node = True
sws = 0
titles = ["time_stamp"]
listr = ["time_stamp"]
for query in df.iloc[:,2]:
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
                       
            temp_data, count, boole, mets, boole2, boole3,save,saves,listr = organize_dataframe(metrics,count ,boole, temp_data, if_same,boole2, len(devices),in_count, mets, boole3,save,saves,query,listr)
            
            in_count += 1
        titles.append(query)

        
    if check =="node":

        temp, instance = organize_instance(query)
        metrics = curly_organizer(query, instance, step)
        metrics = organize_url(metrics, start, end)
        hold = metrics
        metrics = rq.get(metrics)
        data = metrics.json()
        try: 
            if len(data['data']['result']) == 0:
                continue
        except:
            continue
        #sws, boole_node = organize_node_df(metrics, boole_node, sws)
        all_data = np.array(data['data']['result'][0]['values'])
    
        # get metric data
        metric  = all_data[:,1][np.newaxis]
        # get time stamp data
        time_stamp = all_data[:,0][np.newaxis]
    #metric = metric.apply(lambda x: GiB(float(x)), axis=1)
    # for executing just once
        if boole6:
            temp_data2 = np.concatenate((time_stamp.T,metric.T),axis=1)
            boole6=False

    # merge data collectively
        else:
    
            temp_data2 = np.concatenate((temp_data2, metric.T), axis=1)
        
    hold_query = query

try:
    df = pd.DataFrame(temp_data2)
    df.to_csv('nodedede.csv')
except:
    pass

# start title list with one title which is the same for all
# a function to convert byte into megabyte
def div(x):
    x = x/1048576
    y="{:.3f}".format(x)
    y=y+"Mb"
    return y

# get data into dataframe object
#dataframe = pd.DataFrame(save)
try:
    dataframe = pd.DataFrame(save, columns = listr)
#print(titles)
# turn time stamp data into clear data
#dataframe["DateTime"] = dataframe.apply(lambda x: datetime.fromtimestamp(float(x["time_stamp"])), axis=1)

# turn byte data into mb data
#for cols in dataframe.columns:
#    if (cols !=  "time_stamp") and (cols != "DateTime"):
        # usage of created div function
#        dataframe[cols] = dataframe.apply(lambda y: div(float(y[cols])), axis = 1)

# save dataframe into new created cs
    dataframe.to_csv('last_state.csv')

except:
    pass
