from pathlib import Path
from textwrap import dedent
from bs4 import BeautifulSoup

from globalVar import *

def updateCategoryIndex(_pages, _category):
    articles = [
        f"""
        <article>
        <div class="article-info">
            <h2 class="article-title">
            <a href="{page.path.name}">
                {page.title}
            </a>
            </h2>
            <p class="article-date">
            {page.date.replace("-", ".")}.{page.scene}
            </p>
        </div>
        <p class="article-summary">
            {page.note}
        </p>
        </article>
        """
        for page in _pages
        if page.category != "index" and page.title not in hiddenList
    ]

    articleString = "".join(articles)
    categoryIndex = Path(f"{directory / _category}/index.html")
    with open(categoryIndex, "r+", encoding="utf-8") as HTML:
        content = BeautifulSoup(HTML, "html.parser")
        header = content.body.main.header

        oldItems = content.find_all("article")
        for item in oldItems:
            item.extract()

        header.insert_after(BeautifulSoup(dedent(articleString), "html.parser"))
        HTML.seek(0)
        HTML.truncate(0)
        HTML.write(content.prettify(formatter=None))


def updateMainIndex(_pages):
    mainIndex = Path(f"{directory}/index.html")
    articles = [
        f"""
        <article>
        <h1 class="article-title">
            <a href="{page.path}">
            {page.title}
            </a>
        </h1>
        <p class="article-date">
            {page.date.replace("-", ".")}.{page.scene}
        </p>
        <p class="article-summary">
            {page.note}
        </p>
        </article>
        """
        for page in _pages
        if page.category != "index" and page.title not in hiddenList
    ]
    articleString = "".join(articles)
    with open(mainIndex, "r+", encoding="utf-8") as HTML:
        content = BeautifulSoup(HTML, "html.parser")
        target = content.body.main.find(id="column-right")
        target.clear()
        target.append(BeautifulSoup(dedent(articleString), "html.parser"))
        HTML.seek(0)
        HTML.truncate(0)
        HTML.write(content.prettify(formatter=None))
