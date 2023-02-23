from reach_job_instance import *
import numpy as np


# organizes the query, selects and returns query
def curly_organizer(string, selection="{job=node-exporter}", step="5s"):

    # create a string to return
    hold_str = ""
    # booleans for operations

    boole1 = False
    boole2 = False

    # look at letters one by one and organize
    for letter in string:
        # when "{" is encountered, deletes until "}" and places "selection" in
        if letter == "{":
            boole1 = True
            pass
        elif letter=="[":
            boole2 = True
            pass

        if boole1 or boole2:

            if letter == "}":
                hold_str += str(selection)
                boole1 = False
            elif letter == "]":
                hold_str += f"[{step}]"
                boole2 = False
            else:
                pass

        # adds letters that are not in curly branches
        else:

            hold_str += letter


    return hold_str


# organizes the URL and fixes URL request errors
def organize_url(query,start,end,step="5s"):
    
    # define a string to order and return
    url_str = ""
    # get some chars which create problems, 
    # change them to URL utf-8 characters
    for letter in query:

        if letter=="\"":
            url_str += "%22"

        elif letter== "+":
            url_str+= "%2B"

        elif letter=="*":
            url_str+="%2A"

#        elif letter=="-":
#            url_str+="%2D"

        else:
            url_str+= letter

    # return ordered string
    url_str = f"http://localhost:9090/api/v1/query_range?query={url_str}&start={start}&end={end}&step={step}"
    return url_str


# a function to determine if query is libvirt or node
def organize_instance(query, device = reach_device()[0]):
    
    # a boolean for searching the word
    found=False
    check_word = ""
    # if searched word is at the start immediately finish
    if query[0:4] == "node":
        return "node", "{instance="+f'{return_jobs_interfaces("9100")}'+"}"

    if query[0:7] == "libvirt":
        return "libvirt","{instance=" + f'{return_jobs_interfaces("9177")}'+ ",domain=" + f'"{device}"'+"}"

    
    # if not continue searching
    for char in query:
        # as we know if word is not at the start, it is after a "("
        if char == "(":
            found=True
            continue
        if found:
            
            check_word += char
            

        if check_word == "node":
            
            return "node", "{instance="+f'{return_jobs_interfaces("9100")}'+"}"


        if check_word == "libvirt":
            
            return  "libvirt", "{instance=" + f'{return_jobs_interfaces("9177")}'+ ",domain=" + f'"{device}"'+"}"
    return 0, 0


def organize_dataframe(query, count, boole, temp_data, if_same,boole2,device_num=0,incount=0,temp_metrics=0,boole3 = True,save=0,saves=0):
    
    if len(query['data']['result']) == 0:
        pass
    
    else:
        count+=1
        data = query['data']['result'][0]['values']
        #print(data)

        data = np.array(data)
        #print("\n\nQUERY WAS:\t\n", df.iloc[count,1])

        # get metric data
        metric  = data[:,1][np.newaxis]

        # get time stamp data
        time_stamp = data[:,0][np.newaxis]
        #metric = metric.apply(lambda x: GiB(float(x)), axis=1)
        # for executing just once
        if boole:

            if incount == 4:
                boole=False
                
              
            temp_data = np.concatenate((time_stamp.T,metric.T),axis=1)
            #hold = 0
            if boole2:
                    print("boole2 çalıştı")
                    save = temp_data
                    boole2=False
                
            else:
                    print("else executed")
                    save = np.concatenate((save, temp_data), axis=0)
            
            print(save.shape)
        # merge data collectively
        
        #elif incount<5:
        else:
            
            print(incount)
            if boole3:
                saves = metric.T 
                boole3 = False
                
            else:
                saves = np.concatenate((saves,metric.T),axis = 0)
                    
            if incount == 4:
                print(saves.shape)
                print(temp_data.shape)
                save = np.concatenate((save,saves), axis = 1)



    return temp_data, count, boole, temp_metrics, boole2, boole3, save, saves
