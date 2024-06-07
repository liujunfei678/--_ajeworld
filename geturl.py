import json
import math
import requests
from parm import my_parms
import multiprocessing
import os
# my_parm= {
#     'lastViewed': '9359397240638,9359397247781,9359397254529,9359397254659,9359397251733,9359397253294,9359397254109',
#     'userId': 'dd9598b1-4361-4a05-9dc5-00f4ae1b36de',
#     'domain': 'https://ajeworld.com/collections/tops/?page=1',
#     'sessionId': '14e33d51-8dd3-40fb-a20a-03378c59d733',
#     'pageLoadId': 'e118771b-c8dd-41e3-848e-b3fabe4d6df8',
#     'siteId': 'gvh2ln',
#     'page': '1',
#     'bgfilter.ss_hide': '0',
#     'bgfilter.collection_handle': 'tops',
#     'redirectResponse': 'full',
#     'ajaxCatalog': 'Snap',
#     'resultsFormat': 'native'
# }

def get_page(url,my_parm):
    url_list=[]
    res=requests.post(url,json=my_parm).text
    js=json.loads(res)
    try:
        data=js['results']
        for p in data:
            proucturl='https://ajeworld.com/collections/tops'+p['url']
            url_list.append(proucturl)
            print(proucturl)
        return url_list
    except Exception as e:
        print(f'在访问{url}出现了')
        print(f"其具体的pram信息为：{my_parm}")
        print(e)


def get_all_url(url,num,index):
    if not os.path.exists('output'):
        os.makedirs('output')
        print(f"创建文件夹: 'output'")
    all_url=[]
    n=math.ceil(num/28)
    for i in range(n):
        print(f'正在下载第{i+1}页')
        # my_parm['domain']=f'https://ajeworld.com/collections/tops/?page={i+1}'
        # my_parm['page']= f'{i+1}'
        my_parm=my_parms(index,i+1)
        page_url=get_page(url,my_parm)
        all_url+=page_url
        print(page_url)
    with open(f'output/{index}.json','w') as f:
        json.dump(all_url,f)
    return all_url


#
# url='https://gvh2ln.a.searchspring.io/api/search/search.json'
# get_all_url(url,303,'top')

# print(res)
if __name__=="__main__":
    url='https://gvh2ln.a.searchspring.io/api/search/search.json'
    args={
        0:(url,303,'top'),
        1:(url,229,'skirts'),
        2:(url,50,'sale-shorts'),
        3:(url,98,'sale-Pants'),
        4:(url,49,'sale-jackets-coats'),
        5:(url,72,'sale-knitwear-jumpers'),
        6:(url,118,'sale-denim'),
        7:(url,88,'sale-body'),
        # 8:(url,90,'sale-food'),
        8:(url,121,'sale-tees'),
    }
    pool=multiprocessing.Pool(processes=6)
    results = [pool.apply_async(get_all_url, args=args[i]) for i in range(len(args))]
    output=[r.get() for r in results]
    print(output)
    pool.close()
    pool.join()
