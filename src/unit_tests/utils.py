import os

def getclfiles(root):
    return [ os.path.join(dir_path, file) for dir_path, _, file_list in os.walk(root)
                                             for file in file_list if file.endswith('cl') ]

def load_file(file):
    with open(file) as f:
        content = f.read()
        
    return content