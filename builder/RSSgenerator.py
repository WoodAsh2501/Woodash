from bs4 import BeautifulSoup
from pathlib import Path
from textwrap import dedent
from globalVar import *
from minify_html import minify

filePath = Path("../feed.xml")


def readArticle(_page):
    with open(_page.path, "r+", encoding="utf-8") as HTML:
        content = BeautifulSoup(HTML, "html.parser")
        # 删除多余元素
        deleteList = [content.find(id="board"),
                      content.find(class_="article-header"),
                      content.find(id="索引"),
                      ]

        def deleteExistTag(_deleteList):
             for tag in _deleteList:
                  if tag:
                       tag.extract()
        
        deleteExistTag(deleteList)
                       
        article = str(content.body.article)
        article = minify(article).replace("\n", "")
        return dedent(article)

def makeItem(_page):
        if _page.category == "index":
             return ""
        
        if _page.title in hiddenList:
             return ""

        item = f"""
                <item>
                    <title>{_page.title}</title>
                    <category>{_page.category}</category>
                    <pubDate>{_page.date}</pubDate>
                    <description><![CDATA[{readArticle(_page)}]]></description>
                    <link>https://{_page.link}</link>
                </item>
                """
        return item

def generateRSS(_pages):
    RSScontent = f"""<?xml version="1.0" encoding="UTF-8"?>
                <rss version="2.0">
                <!-- RSS万岁! -->
                <channel>
                <title>Woodash * 灰分</title>
                <description>技术与美学与数字花园</description>
                <link>https://woodash.cc</link>
                <language>zh-CN</language>
                <image><url>images/favicon.ico</url></image>
                """
    for page in _pages:
         RSScontent += dedent(makeItem(page))

    RSScontent += f"""    
                </channel>
                </rss>"""
    with open(filePath, "w", encoding="utf-8") as RSSfile:    
        for line in RSScontent.splitlines():
            RSSfile.write(line.strip() + '\n')