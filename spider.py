import sys
import os
import glob
import scrapy
from urllib.parse import urljoin

def urlnorm(base, link=''):
  '''Normalizes an URL or a link relative to a base url. URLs that point to the same resource will return the same string.'''
  new = urlparse(urljoin(base, url).lower())
  return urlunsplit((
    new.scheme,
    (new.port == None) and (new.hostname + ":80") or new.netloc,
    new.path,
    new.query,
    ''))

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

class DRSpider(scrapy.Spider): 
    
    name = 'dr'   
    
    def start_requests(self):
        #get files
        base_path = '/home/wei/data/dr/sample'
        urls_folder_path = os.path.join(base_path, 'urls-en')
        print(urls_folder_path)
        urls_files = get_all_files(urls_folder_path)
        for urls_file_name in urls_files:
            #create folder
            websites_folder_path = os.path.join(base_path, urls_file_name)
            urls_file_path = os.path.join(urls_folder_path, urls_file_name + '.txt')
            if os.path.exists(websites_folder_path):
                remove_folder_contents(websites_folder_path)
            os.makedirs(websites_folder_path)
            #get urls
            urls = get_all_urls(urls_file_path)
            #crawl ursl
            for index, url in enumerate(urls):
                print("urls is {}".format(url))
                yield scrapy.Request(url=url, 
                                    callback=self.parse,
                                    dont_filter=True,
                                    meta = {
                                            'url':url,
                                            'index':index,
                                            'websites_folder_path':websites_folder_path,
                                            'urls_file_name':urls_file_name
                                           })
            
    def parse(self, response):
            if response.status != 200:
                return
            responseURL = response.url
            requestURL = response.meta['url']
            print(responseURL)
            print(requestURL)
            if str(responseURL).__eq__(requestURL):
                file_path = os.path.join(response.meta['websites_folder_path'], str(response.meta['urls_file_name']) + '.' + str(response.meta['index']) + '.html')
                with open(file_path, 'wb') as f:
                    f.write(response.body)
                self.log('Saved file %s' % file_path)
            else:
                yield scrapy.Request(url=responseURL,
                                     callback=self.parse,
                                     dont_filter=True,
                                     meta = {
                                            'url':responseURL,
                                            'index':response.meta['index'],
                                            'websites_folder_path': response.meta['websites_folder_path'],
                                            'urls_file_name':response.meta['urls_file_name']
                                            })