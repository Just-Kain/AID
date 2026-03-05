import requests
from hash_gen import create_cf_query 

methodName = "contest.status"
    
params1 = {
    "groupCode" : "b4hWjnSy2p",
    "contestId" : "657023" ,
    "count" : "5",
    "from" : "1",
    "asManager" : "true",
    }

params = {
    "contestId" : "566" ,
    "from" : "1",
    "count" : "10"
    }

url = create_cf_query(methodName, params1)

ans = requests.get(url)
data = ans.json()
print(url)
print(data)