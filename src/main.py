from organizer import *
import pandas as pd
import requests as rq

df = pd.read_csv('all_queries.csv')
start = "2023-02-20T10:59:25.479Z"
end = "2023-02-20T19:59:25.479Z"
step = "5s"

count = 1
for query in df.iloc[:,2]:
    
    query = curly_organizer(query, organize_instance(query), step)
    query = organize_url(query, start, end)
    sa = input("\nawaiting for an input...: ")
    hold = query
    print(query)
    query = rq.get(query)
    query = query.json()
    print(query)

    print("\n\nQUERY WAS:\t\n", df.iloc[count,1])
    count += 1
