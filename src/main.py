from organizer import *
import pandas as pd
import requests as rq
import numpy as np

# read csv which contains queries
df = pd.read_csv('all_queries.csv')
# get default-recent time data
start, end = give_default_dates()
# start = "2023-02-21T10:59:25.479Z"
# end = "2023-02-21T19:59:25.479Z"
# define default step
step = "5s"
# define a boolean to be used to run a statement for once
one_crap_boolean = True
# get Virtual machine names
devices = reach_device()
# a weird boolean too, to execute a statement once
two_crap_boolean = True

# define a list for to store columns names
titles = ["time_stamp"]

# read queries, organize them and gather their values
for query in df.iloc[:, 2]:
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
            url = curly_organizer(query, instance, step)
            # get data after organizing the url
            url = organize_url(url, start, end)
            # get data using requests modul
            metrics = rq.get(url)
            # turn data into dictionary
            metrics = metrics.json()
            # hold metrics data
            temp_metrics = metrics
            # move depending on if data came
            if len(temp_metric['data']['result']) == 0:
                pass
            # if there is data, go on
            else:
                # parse and dig into data
                data = metrics['data']['result'][0]['values']
                # load data into a numpy array
                data = np.array(data)
                # get metric values
                metric = data[:, 1][np.newaxis]
                # get time stamp values
                time_stamp = data[:, 0][np.newaxis]
                # for executing for 4 times
                if one_crap_boolean:
                    # to create following structure:
                    """ time stamp: ts, metric = m
                    ts (connect) m = a                          a
                                                            (connect)                   
                    ts (connect) m = b                          b        = PART
                                                            (connect)
                    ts (connect) m = c                          c
                    """
                    if in_count == 4:
                        one_crap_boolean = False
                        # 3 vertical, 4 horizontal connections done
                    # horizontally connect
                    temp_data = np.concatenate((time_stamp.T, metric.T), axis=1)

                    # execute for once for first element to connect second element
                    if three_crap_boolean:
                        save = temp_data
                        three_crap_boolean = False
                        titles.append(query)
                    # vertically connect horizontally connected elements
                    else:
                        save = np.concatenate((save, temp_data), axis=0)

                # merge data collectively
                else:
                    # to create following structure:
                    """ Connecting to PART above
                                       metric1
                                      (connect)
                        PART = PART +  metric2
                                      (connect)
                                       metric3
                    """
                    # run once and store first element
                    if four_crap_boolean:
                        saves = metric.T 
                        four_crap_boolean = False
                    # perform operation mentioned above
                    else:
                        saves = np.concatenate((saves, metric.T), axis=0)
                    # if devices' loops' end is reached, add connected metrics
                    if in_count == len(devices):
                        save = np.concatenate((save, saves), axis=1)
                        # append queries into titles
                        titles.append(query)
            # increment at the end of devices loop
            in_count += 1

    # go depending on data
    if check == "node":
        # get instance to run curly organizer function
        temp, instance = organize_instance(query)
        # run curly organizer delete instance and replace it
        url = curly_organizer(query, instance, step)
        # get data after organizing the url
        url = organize_url(url, start, end)
        # hold URL to be used later
        hold = url
        # get data using requests modul
        metrics = rq.get(url)
        # load data into json
        data = metrics.json()
        
        try: 
            if len(data['data']['result']) == 0:
                continue

        except error:
            continue
        # parse data
        all_data = np.array(data['data']['result'][0]['values'])
    
        # get metric data
        metric = all_data[:, 1][np.newaxis]
        # get time stamp data
        time_stamp = all_data[:, 0][np.newaxis]
        # metric = metric.apply(lambda x: GiB(float(x)), axis=1)
        # for executing just once
        if two_crap_boolean:
            temp_data2 = np.concatenate((time_stamp.T, metric.T), axis=1)
            two_crap_boolean = False

        # merge data collectively
        else:
    
            temp_data2 = np.concatenate((temp_data2, metric.T), axis=1)

# save node exporter data
try:
    # load data into a dataframe
    df = pd.DataFrame(temp_data2)
    # save data in csv format
    df.to_csv('node_metrics.csv')
    print("Ma Lord! I saved that uum... ")
    sleep(1)
    print("...")
    sleep(1)
    print("huh! Node data!")
except error:
    print("An error occured while loading file into df and saving file: ", error)
# get data into dataframe object
# dataframe = pd.DataFrame(save)

# save libvirt exporter data
try:
    # load save data into a dataframe
    df = pd.DataFrame(save, columns=titles)
    # turn df into a list to change order of columns
    my_list = df.columns.tolist()
    # load names of devices into a list
    names_devices = []
    for c in range(len(devices)):
        for i in range(int(len(df)/len(devices))):
       
            names_devices.append(devices[c])
    
    df["names"] = names_devices

    # change the order of colums of dataframe
    cols = df.columns.tolist()
    cols = cols[:1] + cols[-1:] + cols[1:-1]
    df = df[cols]
    
    # save data into a csv file
    df.to_csv('libvirt_data.csv')
    print("Sir! I saved that lillb... libvart... libvirt data!")

    # save dataframe into new created cs
    # dataframe.to_csv('last_state.csv')

except error:

    print("Error while loading into csv file: ", error)
    pass
