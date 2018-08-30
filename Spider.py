#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import time
import os
import json
from hashlib import md5



def get_index(page, per):
    """
    打开url得到JSON
    :param page: 页数
    :param per: 数量
    """
    url = 'http://adr.meizitu.net/wp-json/wp/v2/posts?page=' + str(page) + '&per_page=' + str(per)
    print(url)
    try: 
        req = requests.get(url)
        if req.status_code == 200:
            imgs = req.json()
            for item in imgs:
                img_num = item.get('img_num')
                img_url = item.get('thumb_src')
                title = item.get('title')
                for i in range(1, img_num+1):
                    if i >= 10:
                        u = img_url[0:-6]
                        ur = u + str(i) + '.jpg'
                        print("图片总数: {}, 图片地址: {}, 图片标题: {}".format(img_num, ur, title))
                        # 保存到JSON
                        save_to_json(ur, title)
                        # 保存图片到本地
                        save_image(ur)
                    else:
                        u = img_url[0:-5]
                        ur = u + str(i) + '.jpg'
                        print(ur, title)
                        print("图片总数: {}, 图片地址: {}, 图片标题: {}".format(img_num, ur, title))
                        # 保存到JSON
                        save_to_json(ur, title)
                        # 保存图片到本地
                        save_image(ur)
    except ConnectionError:
        pass
        
            

def save_to_json(url, title):
    """
    保存图片链接和标题到JSON
    """
    if url and title:
        results = {
                    'title': title,
                    'url': url
                }
        with open('result.json', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(results, indent=2, ensure_ascii=False))
                    f.close()
                    print('保存到JSON成功')
def save_image(url):
    """
    下载图片保存到本地,文件名进行MD5加密避免重复
    """
    try:
        ir = requests.get(url)
        if ir.status_code == 200:
            content = ir.content
            file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(content)
                    f.close()
                    print('图片下载成功')
    except ConnectionError:
        pass
    
     


def run():
    start = time.time()
    # 一次的数据(最大100)
    per_page = 100
    # 47-1 最多46页
    for i in range(1, 47):
        get_index(i, per_page)
    end = time.time()
    print("程序共耗时: {}".format(end - start))

if __name__ == '__main__':
    run()