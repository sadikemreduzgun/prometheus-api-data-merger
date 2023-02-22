from reach_job_instance import *


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
def organize_instance(query, device = ""):
    
    # a boolean for searching the word
    found=False
    check_word = ""
    # if searched word is at the start immediately finish
    if query[0:4] == "node":
        return "{instance="+f'{return_jobs_interfaces("9100")}'+"}"

    if query[0:7] == "libvirt":
        devices = reach_device()
        print(devices)
        num = int(input("which number of device do you want to check on?: "))
        return "{instance=" + f'{return_jobs_interfaces("9177")}'+ ",domain=" + f'"{devices[num]}"'+"}"

    
    # if not continue searching
    for char in query:
        # as we know if word is not at the start, it is after a "("
        if char == "(":
            found=True
            continue
        if found:
            
            check_word += char
            

        if check_word == "node":
            
            return "{instance="+f'{return_jobs_interfaces("9100")}'+"}"


        if check_word == "libvirt":
            devices = reach_device()
            print(devices)
            num = int(input("which number of device do you want to check on?: "))
            
            return "{instance=" + f'{return_jobs_interfaces("9177")}'+ ",domain=" + f'"{devices[num]}"'+"}"
    return 0
