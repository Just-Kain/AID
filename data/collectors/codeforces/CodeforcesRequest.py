import requests
import hashlib
import time 
import random 

class CFRequests:
    """Базовый класс для работы с Codeforces API"""
    def __init__(self, cf_key: str, cf_secret: str):
        self.cf_key = cf_key
        self.cf_secret = cf_secret 
        
    @staticmethod
    def sha512Hex(message : str) -> str:
        """Создание hash-а"""
        
        encode_message = message.encode('utf-8')
        hash_obj = hashlib.sha512(encode_message)
        hex_digest = hash_obj.hexdigest()
        
        return hex_digest
    
    @staticmethod
    def params_to_string(params : dict):
        """Конвертирует словарь параметров запроса в строку """
        string_params = ""
        
        for key, val in params.items():
            if val == None: continue
            string_params += f"{key}={val}&"
            
        return string_params[:-1]

    @staticmethod
    def sort_params(params : dict):
        """Сортируем параметры по кдючу"""
        sorted_params = dict(sorted(params.items()))
        return sorted_params

    def create_cf_query(self, methodName : str,  params : dict):
        """Создание cf API запроса по введенным методам"""
        
        rand_val = random.randint(100000, 999999)
        
        time_query = f"{time.time():.0f}"
        
        sorted_params = self.sort_params(params)
        
        params_string = self.params_to_string(sorted_params)
        
        unhash_apiSig = f"{rand_val}/{methodName}?apiKey={self.cf_key}&{ params_string }&time={ time_query }#{ self.cf_secret }"
        api_signature = self.sha512Hex(unhash_apiSig)
        
        api_link = f"https://codeforces.com/api/{ methodName }?{ params_string }&apiKey={ self.cf_key }&time={ time_query }&apiSig={ rand_val }{ api_signature }"
                
        return api_link
    
    class contest:
        def __init__(self, parent):
            self.parent = parent
            self.last_url = None
            
        """Работает с методами contest"""
        def status(self, groupCode_=None ,contestId_="566", asManager_=None, handle_=None, from_="1", count_="10", includeSources_=None, showUnofficial_='false'):
            
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
                "includeSources" : includeSources_,
                "showUnofficial" : showUnofficial_,
                }
            
            url = self.parent.create_cf_query(methodName, params)
            self.last_url = url
            response = requests.get(url)
            return response.json()
    
if __name__ == "__main__":
    # cf_key = "..."
    # cf_secret = "..."
    # request = CFRequests(cf_key=cf_key, cf_secret=cf_secret)
    # data = request.contest(request).status(groupCode_="b4hWjnSy2p", contestId_="657023" )
    # print(data)
    ...