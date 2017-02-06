# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
# from SinaArticle_v1 import SinaArticleItem
import json
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

    # LinkExtractors
        # 导航页
    guide_LE = LinkExtractor(allow="/guide/")
        # 排行
    ph_LE = LinkExtractor(allow="/hotnews/")


    rules = (
        Rule(link_extractor=guide_LE, callback="parse_guide"),
        Rule(link_extractor=ph_LE, callback="parse_hotnews"),
    )

    def parse_guide(self, response):
        """
        根据导航页来创建一级类别和二级类别的目录,
            并在目录下创建该类别URL 的txt 文件
        """
        print "====="
        print "parse_guide"
        print "====="

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

    def parse_hotnews(self, response):
        """
        解析新闻排行页面
            获取该页面中获取具体新闻的AJax url
        """
        print "====="
        print "parse_hotnews"
        print "====="

        news_ajaxes = set(response.xpath("//script[contains(@src,'http://top')]/@src").extract())

        for news_ajax in news_ajaxes:
            print "========"
            print news_ajax
            yield Request(url=news_ajax, callback=self.parse_news_json)
            print "========"

    def parse_news_json(self, response):
        """
        解析新闻排行页面Ajax
            获取具体新闻url的集合, 并处理
        """
        print "====="
        print "parse_hotnews"
        print "====="
        full_response = response.body
        json_response = full_response[full_response.index("["): full_response.index("]")+1]
        json_response = json.loads(json_response)
        print "++++++++++++"
        for news_json in json_response:
            # print news_json[u"title"]
            # print news_json[u'url']
            yield Request(news_json[u'url'], callback=self.parse_hotnews_news)
        print "++++++++++++"

    def parse_hotnews_news(self, response):
        """
        处理新闻 -- 排行中的具体新闻页面
        """
        print "====="
        print "parse_hotnews_news"
        print "====="

        filePath = "../Data/新闻/排行/"
        from_url = response.url

        if from_url.startswith("http://news.sina.com.cn"):
            fileName = response.xpath("//h1[@id='artibodyTitle']//text()").extract_first() + '.txt'
            fileContent = ""

            thisNewsPath = filePath + fileName

            news_title = response.xpath("//h1[@id='artibodyTitle']//text()").extract_first()
            news_contents = response.xpath("//div[@class='article article_16']/p/text()").extract()

            fileContent = fileContent + news_title + "\n\n"
            for content in news_contents:
                fileContent = fileContent + content + '\n'

            with open(thisNewsPath, 'w') as thisNewsFile:
                thisNewsFile.write(fileContent)