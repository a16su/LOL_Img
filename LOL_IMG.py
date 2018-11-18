import requests
import os
import json
import threading
from multiprocessing import Pool


class LolPic(object):
    def __init__(self):
        self.hreo_lsit = sid
        self._base_url = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big'

    def get_hero_image_ids(self, hero_id):
        base_url = ''
        pass  # TODO: 修改此处函数，将获取图片方式改为从英雄对应的js文件中获取皮肤id，从而获取皮肤URL，而不是原来的一个一个去拼凑
              # TODO: 英雄对应的js文件URL为: 'https://lol.qq.com/biz/hero/{}.js'.format(hero_name)
              # TODO: 对应的正则为: skins_id = re.findall('"skins":(.*?),"info"', html, re.S)[0]


    def get_img_ulr(self, hero_id, hero_name):
        threads = list()
        for i in range(20):
            last_url = f'00{i}.jpg' if i < 10 else f'0{i}.jpg'
            hreo_url = self._base_url + hero_id + last_url  # 这里通过
            t = threading.Thread(target=self.save_img,
                                 args=(hreo_url, hero_name))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print('\n')

    def save_img(self, url, name):
        response = requests.get(url=url)
        result = dict()
        if os.path.exists(f'./lolimg/{name}'):
            pass
        else:
            os.mkdir(f'./lolimg/{name}')
        if response.status_code == 200:
            with open(f'./lolimg/{name}/{url[-10:-4]}.jpg', 'wb') as f:
                f.write(response.content)
            result['save'] = 200
            result['code'] = 200
            print(f'{name} 第{url[-6:-4]} 张下载完成\n')
        else:
            result['code'] = 404

        return result

    def main(self):
        pool = Pool(processes=4)
        for hero_id, hero_name in self.hreo_lsit.items():
            pool.apply_async(func=self.get_img_ulr, args=(hero_id, hero_name))
        pool.close()
        pool.join()


if __name__ == '__main__':
    file_path = './lol_hreo.txt'
    f = open(file_path, encoding='utf-8').read()  # 加载英雄列表文件
    if f.startswith('\ufeff'):
        f = f.encode('utf8')[3:].decode('utf8')  # 去掉BOM头
    sid = json.loads(f)  # 转换为json文件
    hreo_img = LolPic()
    hreo_img.main()
