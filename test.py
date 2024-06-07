import json
import requests
from bs4 import BeautifulSoup
from time import sleep
from pprint import pprint
MAX_TIME=30
MAX_RETRY=5
RETRY_DALAY=5

def get_res(url):
    retries=0
    while retries<MAX_TIME:
        try:

            res=requests.get(url=url,timeout=MAX_TIME).text
            bs=BeautifulSoup(res,'html.parser')
            return bs
        except requests.exceptions.Timeout:
            print(f"请求超时,正在重试... ({retries + 1}/{MAX_RETRY})")
            retries += 1
            sleep(RETRY_DALAY)
        except requests.exceptions.RequestException as e:
            print(f"请求失败,正在重试... ({retries + 1}/{MAX_RETRY})")
            retries += 1
            sleep(RETRY_DALAY)
    raise Exception(f"无法完成URL {url} 的请求,已达到最大重试次数")

def get_main_pic(bs,url):
    print(f'正在获取{url}下的所有图片')
    pic_list=[]
# print(res)
#     pattern = r'var predictProduct\s*=\s*(\{.*?\})'

    # bs=get_res(url)
    scripts=bs.find_all('script',{'type':'text/javascript'})
    for s in scripts:
        if 'var predictProduct' in str(s):
            # print(s)
            try:

                json_data1=(str(s).split('predictProduct =')[1].strip().split('};')[0]+'}').strip()
                json_data=json.loads(json_data1)
            except:
                print(json_data1)
            # pprint(json_data)
            # match = re.search(pattern, str(s))
            # if match:
            #     predict_product_json = match.group(1).strip()
            #     print(predict_product_json)
                # predict_product = json.loads(predict_product_json)
                # print(predict_product)
    # print(js)
    # pprint(json_data)
    media_list=json_data['media']
    for dic in media_list:
        if dic['alt'] !=None:
            pprint(dic)
            pic='https:'+dic['src']
            # print(pic)
            pic=pic.split('?')[0]
            pic_list.append(pic)
    return pic_list

url='https://ajeworld.com/collections/tops/products/charmed-rosette-ruffle-bustier-misty-rose'
bs=get_res(url)
pic_list=get_main_pic(bs,url)

