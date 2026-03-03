import os
import shutil

encoder='utf-8' 

code_type_lib = {       'c' : 'c++', 
                        'cpp' : 'c++',
                        'py3' : 'py',
                        'py2' : 'py',
                        'pypy3' : 'py',
                        'pypy2' : 'py',
                        'pypy3-64' : 'py',
                        'pas' : 'pas'}
    # Здесь прописаны все поддерживаемые языки для шифрования 
    # На данный момент c++, py, pas

def get_file_paths(folder_path="."):
    file_names = []
    
    for file_name in os.listdir(folder_path):
        file_names.append(folder_path + file_name)
            
    return file_names

def create_and_clear_work_dir(new_dir_name="work_dir"):

    folder_exist = os.path.exists(new_dir_name)
    
    if not folder_exist:
        os.mkdir(new_dir_name)
    else:
        shutil.rmtree(new_dir_name)
        os.mkdir(new_dir_name)
            
def get_extension(path):
    root, extension = os.path.splitext(path)
    return extension

def code_type_definition(code_type):

    try:  
        return code_type_lib[code_type]
    
    except KeyError:
        raise('Warning this code type not supported to encoding!')
    
if __name__ == "__main__":
    test = get_file_paths()
    print(test)
    