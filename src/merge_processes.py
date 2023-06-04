import pandas as pd
from organizer import *
import json
import requests as rq
import numpy as np
from settings import *

global log


def limit_decimal(float_num, float_limit=decimal_limit):

    return round(float(float_num), int(float_limit))


vectorized_limit_decimal = np.vectorize(limit_decimal)


def prepare_node(start,end,step,step_func,server, hold_ins):
    # load csv data into dataframes
    co = 0
    # df = pd.read_csv('all_queries.csv')
    df_nodes = pd.read_csv("nodes2.csv")
    once = True
    # create a list to store the successfully reached data's query names
    columns_node = ["time_stamp"]
    # create a list to store query names of data who had buffer error
    columns_node_buffer_error = []
    # booleans to store initial value in loop
    execute_once = True
    execute_once_buffer_err = True
    alls = 1
    col1 = [1]
    col2 = []
    for name, col in df_nodes.iterrows():

        # get query names and queries
        query_name = col["query_name"]
        query = col["query"]
        # get instance to run curly organizer function
        try:
            instance = f'{return_instance("node", st_num=server)}'
        except:
            instance = hold_ins

        # run curly organizer
        name_query = "node_uname_info{$}"
        url = curly_organizer(query, instance, step_func)
        
        # organize url(request) to prevent clutter
        url = organize_url(url, start, end, step)

        # get data using requests modul
        metric_data_node = rq.get(url).json()
        # check if any error happen
        try:
            # check if there is node metric data
            if len(metric_data_node['data']['result']) == 0:
                log.append(str(datetime.now()) + "\tnode -> " + query_name)
                continue

        except:
            print("Potential time error. Please check if start and end times relevant.")
            log.append("an error occured:\tERROR IN MAIN LOOP! ")
            continue
        
        # load metric data into a numpy array
        metric_data_node = np.array(metric_data_node['data']['result'][0]['values'])
        print("parsed data shape: ", metric_data_node.shape)
        # select metric and time stamp data and get them ready for applying numpy's concatenate module
        metric_ll = vectorized_limit_decimal(metric_data_node[:, 1])
        metric_node = metric_ll[np.newaxis]
        print("metric ayıklanınca shape: ", metric_node.shape)
        time_stamp = metric_data_node[:, 0][np.newaxis]
        print("time stamp ayıklanınca shape: ", time_stamp.shape)

        #metric_df = pd.DataFrame(metric_node.T, columns = [query_name])
        #time_df = pd.DataFrame(time_stamp.T, columns = ["time_stamp"])
        alls = pd.DataFrame(metric_data_node, columns=["time_stamp", query_name])
        mm = pd.DataFrame(metric_node.T, columns=[query_name])
        tt = pd.DataFrame(time_stamp.T, columns=["time_stamp"])

        alls = pd.concat([tt,mm],axis=1)
        print("time stampi ve metriği dataframe'e atayınca data frame shape: ", alls.shape)
        hold_all = alls
        alls = alls.set_index('time_stamp')
        print("\n")
        # hold first data and to merge with metric data
        co += 1
        if execute_once:
            collected_node_data = alls
            execute_once = False
            
            """
            collected_node_data = np.concatenate((time_stamp.T, metric_node.T), axis=1)
            execute_once = False
            columns_node.append(query_name)
            col1.append(query_name)
        """
        else:   
            # try to merge new metric data and old hold data
            try:
                collected_node_data = pd.merge(collected_node_data,alls, left_index=True,how="inner" ,right_index=True)
                print(collected_node_data)
            except:
                print("??")
        hold_ins = instance
    collected_node_data["time_stamp"] = collected_node_data.index
    
    query = "node_uname_info{instance=$}"
    url = curly_organizer(query, instance, step_func)

    # organize url(request) to prevent clutter
    url = organize_url(url, start, end, step)

    # get data using requests modul
    metric_data_node = rq.get(url).json()
    print(metric_data_node) 
    return collected_node_data, 1, metric_data_node['data']['result'][0]['metric']['nodename'], hold_ins


def prepare_libv(start,end,step,step_func,server):

    # get libvirt virtual machines
    devices = reach_device(start, end)
    # get(load into a df) queries and query names of csv file
    df_libvs = pd.read_csv("libvirt_queries.csv")
    # iterate libvirt queries
    columns_libv = []
    execute_for_initial_col = True
    execute_once_initial_block = True

    for name, col in df_libvs.iterrows():

        # get query names and queries
        query_name = col["query_name"]
        query = col["query"]
        # a counter for loop for VMs(devices in instance)
        in_count = 1

        # processes of devices taken by a function
        for device in devices:
            # assign instance to run curly organizer function
            instance = "{instance=" + f'{return_instance("libvirt", st_num=server)}' + ",domain=" + f'"{device}"' + "}"
            # run curly organizer delete instance and replace it
            url = curly_organizer(query, instance, step_func)
            # get data after organizing the url
            url = organize_url(url, start, end, step)

            # get data using requests modul
            metric_data_libv = rq.get(url).json()

            try:
                if len(metric_data_libv['data']['result']) == 0:
                    now = str(datetime.now())

                else:
                    data = metric_data_libv['data']['result'][0]['values']
                    # load data into a numpy array
                    data = np.array(data)
                    # get metric values
                    metric_libv = data[:, 1][np.newaxis]
                    # get time stamp values
                    time_stamp_libv = data[:, 0][np.newaxis]
                    # for executing for 4 times

                    if execute_for_initial_col:
                        # to create following structure:
                        """ time stamp: ts, metric = m
                        ts (connect) m = a                          a
                                                                (connect)                   
                        ts (connect) m = b                          b        =  PART
                                                                (connect)
                        ts (connect) m = c                          c
                        """
                        if in_count == len(devices):
                            execute_for_initial_col = False
                            # 3 vertical, 4 horizontal connections done
                        # horizontally connect
                        temp_data = np.concatenate((time_stamp_libv.T, metric_libv.T), axis=1)

                        # execute for once for first element to connect second element
                        if execute_once_initial_block:
                            libv_processed_data = temp_data
                            execute_once_initial_block = False
                            columns_libv.append(query)
                        # vertically connect horizontally connected elements
                        else:
                            saves = np.concatenate((libv_processed_data, temp_data), axis=0)
                        # if devices' loops' end is reached, add connected metrics
                        if in_count == len(devices):
                            libv_processed_data = np.concatenate((libv_processed_data, saves), axis=1)
                            # append queries into titles
                            columns_libv.append(query_name)

            # catch if anything goes with time
            except:
                print("Potential time error. Please check if start and end time relevant. ")
                log.append("an error occured: \t" + str(datetime.now()) + "\t ERROR IN MAIN LOOP!")
            # if there is data, go on

            # increment at the end of devices loop
            in_count += 1

    return libv_processed_data


def prepare_wind(start,end,step,step_func,server):
    # load csv data into dataframes
    # df = pd.read_csv('all_queries.csv')
    df_windows = pd.read_csv("windows_queries.csv")
    # create a list to store the successfully reached data's query names
    columns_windows = ["time stamp"]
    # create a list to store query names of data who had buffer error
    columns_windows_buffer_error = []
    # booleans to store initial value in loop
    execute_once = True
    execute_once_buffer_err = True
    for name, col in df_windows.iterrows():

        # get query names and queries
        query_name = col["query_name"]
        query = col["query"]
        # get instance to run curly organizer function
        instance = "{instance=" + f'{return_instance("windows", st_num=server)}' + "}"

        # run curly organizer
        url = curly_organizer(query, instance, step_func)

        # organize url(request) to prevent clutter
        url = organize_url(url, start, end, step)

        # get data using requests modul
        metric_data_wind = rq.get(url).json()
        # check if any error happen
        try:
            # check if there is node metric data
            if len(metric_data_wind['data']['result']) == 0:
                log.append(str(datetime.now()) + "\tnode -> " + query_name)
                continue

        except:

            print("Potential time error. Please check if start and end times relevant.")
            log.append("an error occured:\tERROR IN MAIN LOOP! ")
            continue

        # load metric data into a numpy array
        metric_data_wind = np.array(metric_data_wind['data']['result'][0]['values'])

        # select metric and time stamp data and get them ready for applying numpy's concatenate module
        metric_wind = metric_data_wind[:, 1][np.newaxis]
        time_stamp = metric_data_wind[:, 0][np.newaxis]

        # hold first data and to merge with metric data
        if execute_once:
            collected_windows_data = np.concatenate((time_stamp.T, metric_wind.T), axis=1)
            execute_once = False
            columns_windows.append(query_name)

        else:
            # try to merge new metric data and old hold data
            try:
                collected_windows_data_buffer_err = np.concatenate((collected_windows_data, metric_wind.T), axis=1)
            # if shape of arrays are different(when buffer latency) there is an error
            except:
                # sometimes for some queries a few data can't be collected, here it is fixed by doing similar things
                columns_windows_buffer_error.append(query_name)
                if execute_once_buffer_err:
                    collected_windows_data_buffer_err = metric_wind.T
                    execute_once_buffer_err = False
                else:
                    collected_windows_data_buffer_err = np.concatenate((collected_windows_data_buffer_err, metric_wind.T), axis=1)

    return collected_windows_data, columns_windows
