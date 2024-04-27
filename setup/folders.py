import os
import shutil

def initialize_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        
def delete_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)