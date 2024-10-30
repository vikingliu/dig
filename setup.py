from setuptools import setup, find_packages

setup(
    name="dig",
    version="0.1",
    author="viking",
    author_email="viking.liu@qq.com",
    description="NO CODE!!! Base on Scrapy, crawl websites with simple configuration.",

    # 项目主页
    url="http://iswbm.com/",

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages()
)