#
#using selenium to download all website pages.
#

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import util
import numpy as np

logger = util.get_log('data_manager')

class DataManager:
    
    def __init__(self,base_path):

        if not base_path:
            base_path = str(path(pathlib.Path.home(), 'dataset'))

        self.pages_folder_path = os.path.join(base_path, 'pages')
        self.train_path = os.path.join(base_path, 'train'),
        self.valid_path = os.path.join(base_path, 'valid'),
        self.test_path = os.path.join(base_path, 'test'),
        self.urls_folder_path = os.path.join(base_path, 'urls')
        self.map_category_number_to_name = {}
        self.map_category_to_train_number = {}
        self.map_category_to_valid_number = {}
        self.category = 0
        self.train_number = 0
        self.valid_number = 0

    def init_environment(self):            
        
        if os.path.exists(self.pages_folder_path):
            util.remove_folder_contents(self.pages_folder_path)
        os.makedirs(self.pages_folder_path)
        
        if os.path.exists(self.train_path):
            util.remove_folder_contents(self.train_path)
        os.makedirs(self.train_path)
        
        if os.path.exists(self.valid_path):
            util.remove_folder_contents(self.valid_path)
        os.makedirs(self.valid_path)
                
        if os.path.exists(self.test_path):
            util.remove_folder_contents(self.test_path)
        os.makedirs(self.test_path)
                
        if not os.path.exists(self.urls_folder_path):
            print('pls provide url files in a folder named urls')
            return
        
        self.urls_file_names = util.get_all_files(self.urls_folder_path)
        logger.info('init environment')
    
    def load_categories_names(self):
        if not os.path.exists(os.path.join(self.urls_folder_path, 'categories.txt')):
            logger.error("urls folder categories.txt does not exit in {}".format(self.urls_folder_path))
            return
        
        with open(os.path.join(self.urls_folder_path, 'categories.txt'), 'r') as f:
            lines = f.readlines()
            for line in lines:
                number, name = line.strip().split(':')
                number = number.strip('"')
                name = name.strip('"')
                self.map_category_number_to_name[number] = name
        
    def prepare_websites_pages_by_url_files(self):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("permissions.default.image", 2)
        firefox_profile.set_preference("javascript.enabled", True)
        firefox_profile.update_preferences()
        firefox = webdriver.Firefox(firefox_profile)
        firefox.set_page_load_timeout(30)
        
        for url_file_name in self.urls_file_names:
            website_folder_path = os.path.join(self.pages_folder_path, url_file_name)
            url_file_path = os.path.join(self.urls_folder_path, url_file_name +'.txt')
            if os.path.exists(website_folder_path):
                util.remove_folder_contents(website_folder_path)
            os.makedirs(website_folder_path)
            #get urls
            urls = util.get_all_urls(url_file_path)
            #normalizes urls
            urls = map(util.urlnorm, urls)
            #crawl website page
            for index, url in enumerate(urls):
                try:
                    firefox.get(url)
                except:
                    logger.debug('loading {} time out '.format(url))
                time.sleep(10)
                html_path = os.path.join(website_folder_path, url_file_name + '.' + str(index) + '.html')
                with open(html_path, 'w', encoding = 'utf8') as f:
                    try:
                        f.write(firefox.page_source)
                    except:
                        logger.debug('except happened when saving {}'.format(url))
            
        firefox.quit()
        logger.info('got websites pages in {}'.format(self.pages_folder_path))
    
    def prepare_train_data(self):
        if not self.pages_folder_path or not os.path.exists(self.pages_folder_path):
            return
        
        self.category = 0
        self.train_number = 0
        self.map_category_to_train_number = {}
        for root, dirs, files in os.walk(self.pages_folder_path, topdown=True):
            for name in dirs:
                self.category = self.category + 1
                txt_folder_path = os.path.join(self.train_path, name)
                if os.path.exists(txt_folder_path):
                    util.remove_folder_contents(txt_folder_path)
                os.makedirs(txt_folder_path)
            for name in files:
                (short_name, extension) = os.path.splitext(name)
                drive, tail = os.path.split(root)
                self.train_number = self.train_number + len(files)
                self.map_category_to_train_number[tail] = len(files)
                with open(os.path.join(root, name), 'r', encoding = 'utf8') as html:
                    soup = BeautifulSoup(html, "html5lib")
                    text_path = os.path.join(os.path.join(self.train_path, tail), short_name + '.txt')
                    with open(text_path, 'w+', encoding = 'utf8') as txt:
                        for title in soup.find_all('title'):
                            txt.write(title.get_text(strip = True))
                        txt.write('\n')
                        for p in soup.find_all('p'):
                            txt.write(p.get_text(strip = True))
                        
        logger.info('prepared train data in {}'.format(self.train_path))
        logger.info('category is {}, train number is {}'.format(self.category, self.train_number))
        
    def prepare_valid_data(self):
        if not self.train_path or not os.path.exists(self.train_path):
            return
        
        self.valid_number = 0
        self.map_category_to_valid_number = {}
        for root, dirs, files in os.walk(self.train_path, topdown = True):            
            for name in dirs:
                category_folder_path = os.path.join(self.valid_path, name)
                if os.path.exists(category_folder_path):
                    util.remove_folder_contents(category_folder_path)
                os.makedirs(category_folder_path)
            if len(files) > 0:                
                #random pick 20% as valid samples
                valid_count = int(len(files) / 5)
                drive, tail = os.path.split(root)
                self.valid_number = self.valid_number + valid_count
                self.map_category_to_valid_number[tail] = len(files)
                shuf = np.random.permutation(files)
                for i in range(valid_count):
                    os.rename(os.path.join(root, shuf[i]), os.path.join(os.path.join(self.valid_path, tail), shuf[i]))
                    
        logger.info('prepared valid data in {}'.format(self.valid_path))
        logger.info('category is {}, valid number is {}'.format(self.category, self.valid_number))
    


    

