import json
import multiprocessing
from getallpic import main
import os
# 'output/sale-body.json'


def js_save(path):
    print(f'正在下载{path}中的内容！！')
    save_name=path.split('.')[0]+'.txt'
    # print(name)
    all_dic={}
    with open(path,'r') as f:
        data = json.load(f)

    for d in data:
        name=d.split('/')[-1]
        # print(name)
        all_pic_list,other=main(d)
        if other!=[]:
            all_dic[name]=all_pic_list

    with open(save_name,'w') as f:
        json.dump(all_dic,f,indent=4)

# path='output/sale-body.json'
# js_save(path)

def json_file(directory):
    file_path_list=[]
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path=os.path.join(directory,filename)
            file_path_list.append(file_path)
    return file_path_list


path='output/top.json'
js_save(path)
# if __name__=='__main__':
#     dirpath=input('请输入初始文件夹路径：')
#     path='output/top.json'
#     pool=multiprocessing.Pool(processes=6)
#     result=pool.map(js_save,path)
#     pool.close()
#     pool.join()



# path=[]
# list=os.listdir('output')
# for l in list:
#     if l.endswith('.json'):
#         url='output/'+l
#         print(url)
#         path.append(url)
# print(path)









# url='https://ajeworld.com/collections/tops/products/assemblage-asymmetric-top-flora-natura'
# # print(all_pic_list)
# print(main(url))