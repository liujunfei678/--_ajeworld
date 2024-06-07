import requests
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint
from time import sleep
MAX_TIME=30
MAX_RETRY=5
RETRY_DALAY=5
#获取请求
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


#获取其他相关链接
def get_other(bs):
    other_list=[]
    get_the_look=bs.find_all("a",{"class":"grid-view-item__link grid-view-item__image-container full-width-link product-view-link"})
    for i in get_the_look:
        # print(i)
        other='https://ajeworld.com'+i.get('href')
        other_list.append(other)
        # print(other)
    return other_list

#获取主要图片
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
    try:

        media_list=json_data['media']
        for dic in media_list:
            if dic['alt'] !=None:
                # pprint(dic)
                pic='https:'+dic['src']
                # print(pic)
                pic=pic.split('?')[0]
                pic_list.append(pic)
        return pic_list
    except:
        print(f'{url}出错！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！')
        return []


#获取该链接下所有包括相关的图片
def main(url):
    all_pic_list=[]
    bs=get_res(url)
    others=get_other(bs)
    pic_main=get_main_pic(bs,url)
    all_pic_list+=pic_main
    # print(others)
    for other in others:
        # print(other)
        print(f'正在下载相关链接{other}中的相关图片！')
        other_bs=get_res(other)
        other_pic=get_main_pic(other_bs,other)
        all_pic_list+=other_pic
    return all_pic_list,others

# url='https://ajeworld.com/collections/tops/products/assemblage-asymmetric-top-flora-natura'
# print(all_pic_list)
# print(main(url))
# get_main_pic(url)
# url=('https://ajeworld.com/collections/sale-body/products/parfum-corset-crop-knit-top-black')
# bs=get_res(url)
# print(get_other(bs))



