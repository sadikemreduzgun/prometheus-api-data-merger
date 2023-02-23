import yaml
import json
import requests as rq
import json


# a function to return interfaces and jobs
def return_jobs_interfaces(which=""):
    # assign the path of prometheus's yaml file
    path = "/etc/prometheus/prometheus.yml"
    # a dictionary to keep data
    jobs_instances = {}
    # open yaml file
    with open(path, "r") as file:
        # check if sth is wrong
        try:
            # load data
            data = yaml.safe_load(file)
            # parse and load jobs and instances into the dictionary
            for num in range(len(data["scrape_configs"])):
                jobs_instances[data["scrape_configs"][num]["job_name"]] = data["scrape_configs"][num]["static_configs"][0]["targets"][0]
        
        # be sure nothing is wrong
        except yaml.YAMLError as exc:
            print(exc)
    # close file
    file.close()

    if len(which) != 0:
        for var in jobs_instances.values():
            check_word = ""
            found = False
            for char in var:
    
                if char == ":":
                    found=True
                    continue

                if found:
                    check_word += char
                    
                if str(check_word) == which:
                    
                    return f'"{var}"'
                    break
    else:

        return f'"{jobs_instances}"'


def reach_device():

    domains = []
    query = "libvirt_domain_block_stats_allocation"
    url = f"http://localhost:9090/api/v1/query?query={query}"
        
    data = rq.get(url)
    data = data.json()
    #data = json.dumps(data, indent=4)

    for i in (range(len(data["data"]["result"]))):
        hold = data["data"]["result"][i]["metric"]["domain"]
        domains.append(hold)
    
    return domains


print(reach_device())

