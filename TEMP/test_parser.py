
"""  
cpp_var_type_lib = ['long', 'int', 'string', 'bool', 'float', 'double', 'map']

cpp_var_dict = {}

def cpp_hash_var(var : str) -> str:
    return '#'+var+str(len(cpp_var_dict))

def cpp_string_var_defines(old_string : str) -> str:

    new_string = old_string.strip()
    
    if new_string == '':
        return ''
    
    if '#include' in new_string or 'using ' in new_string:
        return ''
     
    for var in cpp_var_type_lib:
        if var in new_string:
            catch_var = new_string.replace(var, '').replace(';', '').strip()
            list_var = catch_var.split(',')
            for i in list_var:
                exist_equal = max(i.find('='), i.find('('))
                if exist_equal != -1:
                    i = i[:exist_equal]
                i = i.strip()
                cpp_var_dict[i] = cpp_hash_var(var)
                new_string = new_string.replace(i, cpp_var_dict[i])
            
            break
    
    return new_string + '\n'
 
def cpp_encoder(content : str) -> str: 

    temp_string = content.replace("    ", '').replace('long long', 'long').split('\n')
    new_content = ''
    
    for i in temp_string:
        new_string = cpp_string_var_defines(i)
        new_content += new_string
        
    key_list = list(cpp_var_dict.keys())
    key_list.sort()
    key_list.reverse()
    
    for key in key_list:
        new_content = new_content.replace(key, cpp_var_dict[key])
    
    return new_content
"""

"""
Мусор выше, можно использовать для сравнивания кода
"""

import ast

code = """
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def fibonacci(n, mod):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, (a + b) % mod
    return b

MOD = 10**9 + 7


n = int(input())
a = list(map(int, input().split()))
"""

tree = ast.parse(code)

for node in ast.walk(tree):
    if isinstance(node, ast.Name):
        # id содержит имя переменной
        print(f"Имя: {node.id}, Контекст: {type(node.ctx).__name__}")