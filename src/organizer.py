# import package and library
from reach_job_instance import *
import numpy as np


# organizes the query, selects and returns query
def curly_organizer(string, selection="{job=node-exporter}", step="5s"):

    # create a string to return
    hold_str = ""
    # booleans for operations
    # run once and if searched item is found, delete it.
    boole1 = False
    boole2 = False

    # look at letters one by one and organize
    for letter in string:
        # when "{" is encountered, delete until "}"
        # then place in "selection"
        if letter == "{":
            boole1 = True
            pass
        elif letter=="[":
            boole2 = True
            pass
        # place chosen step time into
        if boole1 or boole2:

            if letter == "}":
                hold_str += str(selection)
                boole1 = False
            elif letter == "]":
                # after deleting [some time]
                # place in desired time
                hold_str += f"[{step}]"
                boole2 = False
            else:
                pass

        # adds letters that are not in curly branches
        else:

            hold_str += letter

    # return the hold_str string after performing step choice of some query functions
    return hold_str


# organizes the URL and fixes URL request errors
# do it because sometimes it makes problem of request
def organize_url(query,start,end,step="5s"):
    
    # define a string to order and return
    url_str = ""
    # get some chars which create problems, 
    # change them to URL utf-8 characters
    for letter in query:
        # if there is (") character, change it to "%22"
        if letter=="\"":
            url_str += "%22"
        # if there is "+" character, change it to "%2B"
        elif letter== "+":
            url_str+= "%2B"
        # if there is "*" character, change it to %2A
        elif letter=="*":
            url_str+="%2A"

#        elif letter=="-":
#            url_str+="%2D"
        # if there is no character which we search, don't change and add
        else:
            url_str+= letter

    # return ordered string-url
    url_str = f"http://localhost:9090/api/v1/query_range?query={url_str}&start={start}&end={end}&step={step}"
    return url_str


# a function to determine if query is libvirt or node
def organize_instance(query, device = reach_device()[0]):
    
    # a boolean for searching the word
    found=False
    # define an empty string to be used
    check_word = ""
    # if searched word is at the start immediately decide and finish
    # if first 4 letters form node, return instance which is created
    if query[0:4] == "node":
        # return instance created by return_instance function
        return "node", "{instance="+f'{return_instance("node")}'+"}"
    # if first 7 letters form libvirt, return instance which is created
    if query[0:7] == "libvirt":
        # return instance created bt return_instance function
        return "libvirt","{instance=" + f'{return_jobs_interfaces("libvirt")}'+ ",domain=" + f'"{device}"'+"}"

    
    # if not continue searching
    for char in query:
        # as we know if word is not at the start, it is after a "(" because it must be a query function
        if char == "(":
            # search for "(" if found, step on this execution of for loop
            found=True
            continue
        # search letters after "(" character
        if found:
            
            check_word += char
            
        # if "node" is found, return instance as stated
        if check_word == "node":
            
            return "node", "{instance="+f'{return_jobs_interfaces("node")}'+"}"

        # if "libvirt" is found, return instance as stated
        if check_word == "libvirt":
            
            return  "libvirt", "{instance=" + f'{return_jobs_interfaces("libvirt")}'+ ",domain=" + f'"{device}"'+"}"
    # if can't be found return error
    return -1, -1


# organize libvirt data
def organize_dataframe(query, count, boole, temp_data, if_same,boole2,device_num=0,incount=0,temp_metrics=0,boole3 = True,save=0,saves=0,urs ="",lists=[]):
    
    if len(query['data']['result']) == 0:
        pass
    
    else:
        count+=1
        data = query['data']['result'][0]['values']

        data = np.array(data)

        metric  = data[:,1][np.newaxis]

        time_stamp = data[:,0][np.newaxis]
        # for executing just once
        if boole:

            if incount == 4:
                boole=False
                
                          
            temp_data = np.concatenate((time_stamp.T,metric.T),axis=1)
            #hold = 0
            if boole2:
                    save = temp_data
                    boole2=False
                    lists.append(urs)
                
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
                    
            if incount == 4:
                save = np.concatenate((save,saves), axis = 1)
                lists.append(urs)


    return temp_data, count, boole, temp_metrics, boole2, boole3, save, saves, lists
