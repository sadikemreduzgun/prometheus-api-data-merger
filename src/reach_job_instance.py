import yaml
import json
import requests as rq
import json
from reach_time import *


# a function to return interfaces and jobs
def return_jobs_interfaces(which="",start=give_default_dates()[1],end=give_default_dates()[0]):
    
    query="node_load1"
    url = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=30s"

    data = rq.get(url)
    data = data.json()
    if which == "node":
        query="node_load1"
        url = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=30s"

        data = rq.get(url)
        data = data.json()
        result = data['data']['result'][0]['metric']['instance']
        return f'"{result}"'
    
    elif which == "libvirt":

        query="libvirt_domain_block_stats_allocation"
        url = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=30s"

        data = rq.get(url)
        data = data.json()

        result = data['data']['result'][0]['metric']['instance']

        return f'"{result}"'
        #data = json.dumps(data, indent=4)

    else:
        return -1


def reach_device(start=give_default_dates()[1],end=give_default_dates()[0]):

    domains = []
    query = "libvirt_domain_block_stats_allocation"
    url = f"http://localhost:9090/api/v1/query_range?query={query}&start={start}&end={end}&step=3m"
        
    data = rq.get(url)
    data = data.json()
    #data = json.dumps(data, indent=4)

    for i in (range(len(data["data"]["result"]))):
        hold = data["data"]["result"][i]["metric"]["domain"]
        domains.append(hold)
    
    return domains


#print(reach_device())
