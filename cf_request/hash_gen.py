import hashlib
import time 
from cf_request.cf_setings import cf_key, cf_secret
import random 

def sha512Hex(message : str) -> str:
    """Создание hash-а"""
    
    encode_message = message.encode('utf-8')
    hash_obj = hashlib.sha512(encode_message)
    hex_digest = hash_obj.hexdigest()
    
    return hex_digest
    
def params_to_string(params : dict):
    """Конвертирует словарь параметров запроса в строку """
    
    string_params = ""
    
    for key, val in params.items():
        string_params += f"{key}={val}&"
        
    return string_params[:-1]

def create_cf_query(methodName : str,  params : dict):
    
    rand_val = random.randint(100000, 999999)
    
    time_query = f"{time.time():.0f}"
    
    params_string = params_to_string(params)
    
    unhash_apiSig = f"{rand_val}/{methodName}?apiKey={cf_key}&{ params_string }&time={ time_query }#{ cf_secret }"
    api_signature = sha512Hex(unhash_apiSig)
    
    api_link = f"https://codeforces.com/api/{ methodName }?{ params_string }&apiKey={ cf_key }&time={ time_query }&apiSig={ rand_val }{ api_signature }"
            
    return api_link
     
if __name__ == "__main__":
    
    methodName = "contest.status"
    
    qu = {
        "contestId" : "657023" ,
        "groupCode" : "b4hWjnSy2p"
        }
    
    query_link = create_cf_query(methodName=methodName, params=qu)
    print(query_link)
   
   