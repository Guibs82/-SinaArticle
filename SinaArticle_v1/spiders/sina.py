# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from SinaArticle_v1 import SinaArticleItem
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""
    一级类别标题:
        类别所在模块 -- //h3[@class='tit02']
        类别名 -- .//text()
        类别url -- ./a/@href   [地方站, 产品, 客户端 没有url]

    二级类别标题:
        类别所在模块 -- ./following-sibling::ul/li/   [一级类别相邻的ul]
        类别名 -- ./following-sibling::ul/li/a/text()
        类别url -- ./following-sibling::ul/li/a/@href
"""

class SinaSpider(CrawlSpider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']


    rules = (

    )

    def parse(self, response):
        """
        根据导航页来创建一级类别和二级类别的目录,
            并在目录下创建该类别URL 的txt 文件
        """
        parentTags = response.xpath("//h3[@class='tit02']")
        for parentTag in parentTags:
            parentTitle = parentTag.xpath(".//text()").extract_first()
            parentUrl = parentTag.xpath("./a/@href").extract_first()
            # 创建一级目录
                # 1. 通过一级类别确定一级文件夹名
            parentDirPath = "../Data/" + parentTitle
                # 2. 如果该文件夹不存在则创建文件夹
            if not os.path.exists(parentDirPath):
                os.makedirs(parentDirPath)
                # 3.创建存储该一级类别URL 的文件
            if parentUrl is None:
                parentUrl = "该一级类别没有URL"
            with open(parentDirPath + '/' + parentTitle + '.txt', 'w') as parentUrlTxT:
                parentUrlTxT.write(parentUrl)

            # 创建该一级类别的二级类别目录
                # 1. 该一级类别下的二级类别Tags
            subTags = parentTag.xpath("./following-sibling::ul/li/a")
            for subTag in subTags:
                # 2. 获取二级类别名, 并创建不存在的二级文件夹
                subTitle = subTag.xpath("./text()").extract_first()
                subDirPath = "../Data/" + parentTitle + '/' + subTitle
                if not os.path.exists(subDirPath):
                    os.makedirs(subDirPath)
                # 3. 创建存储该一级类别URL 的文件
                subUrl = subTag.xpath("./@href").extract_first()
                if subUrl is None:
                    subUrl = "该一级类别没有URL"
                with open(subDirPath + '/' + subTitle + '.txt', 'w') as subUrlTxT:
                    subUrlTxT.write(subUrl)