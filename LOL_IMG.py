import re
import requests
import os
import json
import threading
from multiprocessing import Pool


class LolPic:
    def __init__(self):
        self.hero_data = hero_data
        self._base_url = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big'

    def get_hero_image_ids(self, hero_name):
        """
        从英雄对应的js文件中获取皮肤id和名称
        :param hero_name: 英雄的名称
        :return: skin_id_dict :一个字典列表，元素为皮肤对应的数据
        :retype: [{},{},...]
        """
        hero_js_url = 'https://lol.qq.com/biz/hero/{}.js'.format(hero_name)
        html = requests.get(hero_js_url)
        if html.status_code == 200:
            html.encoding = 'utf-8'
            skin_id_dict_str = re.findall('"skins":(.*?),"info"', html.text, re.S)[0]
            skin_id_dict_list = json.loads(skin_id_dict_str)
            yield from skin_id_dict_list  # type: [{}, {}]
        else:
            print(f'{hero_name}.js 请求出错')

    def download_hero_image(self, hero_name):
        """
        图片下载函数，通过调用self.get_hero_image_ids来获取英雄对应的数据，
        然后通过self.save_image来请求并保存图片
        :param hero_name :英雄的名字->Aatrox...
        :type :str
        :return None
        """
        print(f'\n{"*"*20}开始下载 {hero_name}{"*"*20}')
        threads = list()
        for skin_data in self.get_hero_image_ids(hero_name):
            hero_skin_url = self._base_url + skin_data["id"] + '.jpg'
            hero_skin_name = skin_data["name"]
            hero_skin_name = re.sub('[\\\\/:*?\"<>|]', '', hero_skin_name)
            threads.append(threading.Thread(target=self.save_img,
                                            args=(hero_skin_url, hero_skin_name, hero_name)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print(f'{"*"*20}{hero_name} 下载完成{"*"*20}\n')

    def save_img(self, hero_skin_url, hero_skin_name, hero_name):
        """
        图片保存函数
        :param hero_skin_url: 英雄皮肤链接
        :param hero_skin_name: 英雄皮肤名称
        :param hero_name: 英雄名字，用来生成对应的文件夹
        :return: None
        """
        response = requests.get(url=hero_skin_url)
        if os.path.exists(f'./lolimg/{hero_name}'):
            pass
        else:
            os.makedirs(f'./lolimg/{hero_name}')
        if response.status_code == 200:
            with open(f'./lolimg/{hero_name}/{hero_skin_name}.jpg', 'wb') as f:
                f.write(response.content)
            print(f'{hero_name} {hero_skin_name} 下载完成')
        else:
            print(f'{hero_name} {hero_skin_name} 下载失败，url为{hero_skin_url}')

    def main(self):
        """
        主函数，用来进行多进程调用，4个进程
        :return: None
        """
        pool = Pool(processes=4)
        for _, hero_name in self.hero_data.items():
            pool.apply_async(func=self.download_hero_image, args=(hero_name,))
        pool.close()
        pool.join()


if __name__ == '__main__':
    fp = open('./lol_hero.json', 'r', encoding='utf-8')
    hero_data = json.load(fp)  # 读取英雄的id和名称
    fp.close()
    hero_img = LolPic()
    hero_img.main()
