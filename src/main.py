from organizer import *
import pandas as pd
import requests as rq
import numpy as np

df = pd.read_csv('all_queries.csv')

start,end = give_default_dates()
print(start,end)
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
            holdidi = metrics 
            if_same = (hold_query == query)

            if len(holdidi['data']['result']) == 0:
                pass
            
            else:
                count+=1
                data = metrics['data']['result'][0]['values']

                data = np.array(data)

                metric  = data[:,1][np.newaxis]

                time_stamp = data[:,0][np.newaxis]
                # for executing just once
                if boole:

                    if in_count == 4:
                        boole=False
                        
                                  
                    temp_data = np.concatenate((time_stamp.T,metric.T),axis=1)
                    #hold = 0
                    if boole2:
                            save = temp_data
                            boole2=False
                            listr.append(query)
                        
                    else:
                            save = np.concatenate((save, temp_data), axis=0)
                    
                    print(save.shape)
                # merge data collectively
                
                #elif incount<5:
                else:

                    if boole3:
                        saves = metric.T 
                        boole3 = False
                        
                    else:
                        saves = np.concatenate((saves,metric.T),axis = 0)
                            
                    if in_count == 4:
                        save = np.concatenate((save,saves), axis = 1)
                        listr.append(query)

                      
#            temp_data, count, boole, mets, boole2, boole3,save,saves,listr = organize_dataframe(metrics,count ,boole, temp_data, if_same,boole2, len(devices),in_count, mets, boole3,save,saves,query,listr)
            
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


df = pd.DataFrame(temp_data2)
df.to_csv('nodedede.csv')
print(listr)
def div(x):
    x = x/1048576
    y="{:.3f}".format(x)
    y=y+"Mb"
    return y


# get data into dataframe object
#dataframe = pd.DataFrame(save)
try:

    df = pd.DataFrame(save, columns = listr)
    my_list = df.columns.tolist()
    names_devices = []
    c = 0
    for c in range(len(devices)):
        for i in range(int(len(df)/len(devices))):
       
            names_devices.append(devices[c])


    
    df["names"] = names_devices
    
    print("worrkrds")
    cols = df.columns.tolist()
    cols = cols[:1] + cols[-1:] + cols[1:-1]
    df = df[cols]
    print(df)
    df.to_csv('libvirt_data.csv')
    print("sir! I saved it!")

    # save dataframe into new created cs
    dataframe.to_csv('last_state.csv')

except:
    pass
