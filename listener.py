import time 
import os 
import threading
from datetime import datetime
import requests
repos  =  ['/home/yyy/workplace'] 
sourcecodes = ['cpp', 'py', 'c', 'cpp', 'java', 'js', 'html']

def get_all_file(dir):

    res = []
    contents = os.listdir(dir)
    for item in contents:
        item_path = os.path.join(dir, item)
        if os.path.isdir(item_path):
            res.extend(get_all_file(item_path))
        else:
            res.append(item_path)
    return res
files = []
for repo in repos:
    repo_files = get_all_file(repo)
    files.extend([ f for f in repo_files if len(f.split('.'))==2 and f.split('.')[1] in sourcecodes])



def count_lines(path):
    with open(path) as f:
        content = f.read(1024*1000)
        cnt = content.count('\n')
    filetype = path.split('.')[1]
    return (filetype, cnt)


def update(filecounts, element):
    if element[0] in filecounts:
        filecounts[element[0]] += element[1]
    else:
        filecounts[element[0]] = element[1]


def getinfo(files,res, index):
    counter = {}
    for f in files:
        update(counter, count_lines(f))
    res[index] = counter
    
def merge(dict1, dict2):
    '''
        merge dict2 to dict1
    '''

    for key in dict2:
        if key in dict1:
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1



# print(merge(getinfo(files[:10]),getinfo(files[10:])))
def multithread_readinfo(files):
    threads = []
    res = [{} for _ in range(6)]
    for start in range(0,6):
        thread = threading.Thread(target=getinfo, args=(files[start::6],res,start))
        threads.append(thread)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    for x in res[1:]:
        merge(res[0], x)
    print(res[0])
    return res[0]




res =  multithread_readinfo(files)
url  = 'http://106.15.176.216/api_v1/codeInfo'
json = {
    'username':'yellowbluewhite',
    'password':'xwt123456789',
    'data':res
}
r = requests.post(url, json=res)
print(r)