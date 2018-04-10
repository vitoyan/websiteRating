import sys
import os
import glob
import logging
from url_normalize import url_normalize

def urlnorm(url):
    return url_normalize(url)
  

def get_all_files(path):
    files = []
    if path:
        full_paths = [full_path for full_path in glob.glob(os.path.join(path, '*.txt'))]
        for full_path in full_paths:
            rel_path, file_name = os.path.split(full_path)
            (short_name, extension) = os.path.splitext(file_name)
            if short_name.isdigit():
                files = files + [short_name]
    return files      

def get_all_urls(path):
    urls = []
    if path:
        with open(path) as f:
            urls = [line.rstrip() for line in f]
    return urls

def remove_folder_contents(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

def get_log(log_name, logLevel = logging.DEBUG):
    logger = logging.getLogger(log_name)
    logger.setLevel(logLevel)
    
    # create console handler and set level to debug
    ch = logging.FileHandler(log_name + '.log')
    ch.setLevel(logLevel)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    
    return logger
    


            
    