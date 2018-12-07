## LOL上英雄皮肤图片下载

闲的没事干，突然想到lol皮肤这个东西，然后就写了一个爬虫程序。刚开始时写的很垃圾，
对于有每个英雄有多少个皮肤完全靠看请求是否成功。后来仔细看了一下网站上的js，发现每个
英雄都有一个对应的js文件，里面是该英雄的相关数据，英雄定位、各项数据、皮肤名称以及链接等，so改进了一下代码，后面又试了一下用协程来爬。
golang版本的README[在这里](./README_GOLANG.md)
## 使用方法
1. `pip install pipenv`使用`pipenv`来管理虚拟环境
2. `pipenv install`安装模块
3. `pipenv shell`激活虚拟环境或者走第四步
   - `python LOL_IMG.py` 或者 `python lol_img_aiohttp.py`
4. `pipenv run LOL_IMG.py`或者`pipenv run lol_img_aiohttp.py`在不激活虚拟环
境的情况下运行代码
5. 图片会被下载到程序所在目录下的`lolimage`目录下，每个英雄都会创建一个文件夹。

## 将来计划
没什么意外python版本不会再更新了，等我过几天写一个golang版本的，这样就可以直接使用编译后的程序，而不需要python环境-已完成

