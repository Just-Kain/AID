import requests
from cf_request.hash_gen import create_cf_query 

class cf_requests():
    class contest():
        """Работает с методами contest"""
        def status(groupCode_=None ,contestId_="566", asManager_=None, handle_=None, from_="1", count_="10", includeSources_=None):
            
            """Возвращает попытки для указанного соревнования. Дополнительно может вернуть попытки указанного пользователя.\n
            Возвращает список объектов Submission, отсортированных по убыванию id попытки"""
            
            methodName = "contest.status"
            
            params = {
                "groupCode" : groupCode_,
                "contestId" : contestId_ ,
                "asManager" : asManager_,
                "handle" : handle_,
                "from" : from_,
                "count" : count_,
                "includeSources" : includeSources_
                }
            
            url = create_cf_query(methodName, params)
            requests_ans = requests.get(url)
            data = requests_ans.json()
            return data
    
if __name__ == "__main__":
    data = cf_requests.contest.status()
    print(data)