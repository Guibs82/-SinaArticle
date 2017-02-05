# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SinaArticleItem(scrapy.Item):
    """
    一级类别标题:
        parentTitle
    一级类别URL:
        parentUrl
    一级类别存储路径:
        parentFilePath

    二级类别标题:
        subTitle
    二级类别URL:
        subUrl
    二级类别存储路径:
        subFilePath

    文章链接:
        articleUrl
    文章标题:
        articleTitle
    文章内容:
        articleContent
    """
    parentTitle = scrapy.Field()
    parentUrl = scrapy.Field()
    parentFilePath = scrapy.Field()

    subTitle = scrapy.Field()
    subUrl = scrapy.Field()
    subFilePath = scrapy.Field()

    articleUrl = scrapy.Field()
    articleTitle = scrapy.Field()
    articlePath = scrapy.Field()