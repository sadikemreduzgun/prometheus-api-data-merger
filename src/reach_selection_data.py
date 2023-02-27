import json
import requests as rq
import json
from reach_time import *


# a function to return interfaces and jobs, gets functionally-updatet start time
def return_jobs_interfaces(which="",start=give_default_dates()[0],end=give_default_dates()[1]):
    
    if which == "node":
        # assign query
        query="node_load1"
        # load dates and query into URL
        url = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=30s"
        
        # get data using requests
        data = rq.get(url)
        # turn data into dictionary
        data = data.json()

        # parse data to get instance
        result = data['data']['result'][0]['metric']['instance']
        # return reached instance
        return f'"{result}"'
    
    elif which == "libvirt":
        # assign query
        query="libvirt_domain_block_stats_allocation"
        # load query and time data into URL
        url = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=30s"
        
        # get data using requests library
        data = rq.get(url)
        # turn data into dictionary to be able to pars
        data = data.json()

        # parse data to get instance
        result = data['data']['result'][0]['metric']['instance']
        
        # return data
        return f'"{result}"'
    
    # if something goes wrong return error
    else:
        return -1


# a function to reach domain names gets recent time data
def reach_device(start=give_default_dates()[0],end=give_default_dates()[1]):
    
    # define an empty list
    domains = []
    # define a query
    query = "libvirt_domain_block_stats_allocation"
    # load the query and the taken time data into an URL
    url = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=3m"
    
    # get data using api
    data = rq.get(url)
    # turn data into a dictionary
    data = data.json()
    #data = json.dumps(data, indent=4)
    
    # parse into the data, reach machine names
    for i in (range(len(data["data"]["result"]))):
        
        hold = data["data"]["result"][i]["metric"]["domain"]
        # add machine names into defined empty-list
        domains.append(hold)
    
    # return domain names(virtual machine names)
    return domains

