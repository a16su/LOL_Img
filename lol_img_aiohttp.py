#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: daning
"""
该文件为lol英雄图片爬虫的aiohttp版本，尝试之作
流程和多线程版本一样
"""

import asyncio
import os
import json
import aiohttp
import re

base_url = 'http://ossweb-img.qq.com/images/lol/web201310/skin/big'


async def get_hero_image_ids(hero_name):
    hero_js_url = 'https://lol.qq.com/biz/hero/{}.js'.format(hero_name)
    async with aiohttp.ClientSession() as session:
        async with session.get(hero_js_url) as response:
            if response.status == 200:
                response = await response.text(encoding='utf-8')
                skin_id_dict_str = re.findall('"skins":(.*?),"info"', response, re.S)[0]
                skin_id_dict_list = json.loads(skin_id_dict_str)
                return skin_id_dict_list


async def download_hero_image(hero_name):
    print(f'\n{"*"*20}开始下载 {hero_name}{"*"*20}')
    taske = list()
    for skin_data in await get_hero_image_ids(hero_name):
        hero_skin_url = base_url + skin_data["id"] + '.jpg'
        hero_skin_name = skin_data["name"]
        hero_skin_name = re.sub('[\\\\/:*?\"<>|]', '', hero_skin_name)
        print(f'{hero_name}-> {hero_skin_name}')
        # taske.append(asyncio.ensure_future(save_img(hero_skin_url,
        #                                             hero_skin_name,
        #                                             hero_name)))
        # await asyncio.gather(*taske)
    print(f'{"*"*20}{hero_name} 下载完成{"*"*20}\n')


async def save_img(hero_skin_url, hero_skin_name, hero_name):
    if os.path.exists(f'./lolimg/{hero_name}'):
        pass
    else:
        os.makedirs(f'./lolimg/{hero_name}')
    async with aiohttp.ClientSession() as session:
        async with session.get(hero_skin_url) as response:
            if response.status == 200:
                with open(f'./lolimg/{hero_name}/{hero_skin_name}.jpg', 'wb') as f:
                    connect = await response.content.read()
                    f.write(connect)
                print(f'{hero_name} {hero_skin_name} 下载完成')
            else:
                print(f'{hero_name} {hero_skin_name} 下载失败，url为{hero_skin_url}')


def main():
    tasks = list()
    loop = asyncio.get_event_loop()
    for _, hero_name in hero_data.items():
        tasks.append(asyncio.ensure_future(download_hero_image(hero_name=hero_name)))
    loop.run_until_complete(asyncio.gather(*tasks))


if __name__ == '__main__':
    fp = open('./lol_hero.json', 'r', encoding='utf-8')
    hero_data = json.load(fp)  # 读取英雄的id和名称
    fp.close()
    main()
