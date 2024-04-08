from pathlib import Path
from textwrap import dedent, indent
from bs4 import BeautifulSoup
from bs4 import Comment
from bs4.formatter import HTMLFormatter


categorys = ["notes", "weekly", "essays", "experience", "records"]
categoryDict = {
    "essays": "杂谈",
    "weekly": "周报",
    "experience": "体验",
    "records": "琐记",
    "notes": "笔记",
}
attrDict = {
    "note": "woodash-note",
    "tucao": "woodash-tucao",
    "scene": "woodash-scene",
    "date": "date",
}

folder = Path(".")

class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v

class Page:
    def __init__(
        self,
        title="",
        category="",
        note="",
        tucao="",
        scene="",
        date="",
        path="",
        style="",
    ):
        self.title = title
        self.category = category
        self.note = note
        self.tucao = tucao
        self.scene = scene
        self.date = date
        self.path = path
        self.style = style

    def edit(self):

        def setStyle(self):
            with open(self.path, "r+", encoding="utf-8") as HTML:
                content = BeautifulSoup(HTML, "html.parser")
                head = content.head
                styleList = head.find_all("link", rel="stylesheet")
                styleList = map(str, styleList)
                self.style = styleList

        def setAttrs(self):
            with open(self.path, "r+", encoding="utf-8") as HTML:
                content = BeautifulSoup(HTML, "html.parser")
                head = content.head

                attrs = (attr for attr in attrDict.keys())

                for attr in attrs:
                    attrName = attrDict[attr]
                    tag = head.find("meta", attrs={"name": attrName})
                    if tag:
                        setattr(self, attr, tag["content"])

        def addWelcome(self):
            with open(self.path, "r+", encoding="utf-8") as HTML:
                content = BeautifulSoup(HTML, "html.parser")
                welcomeMsg = """
                          欢迎来到花园杂乱无章的*苗圃*！
                          请随意看看吧。
                          """
                welcomeComment = Comment(dedent(welcomeMsg))

                hasComment = type(content.contents[0]) == Comment
                if not hasComment:
                    content.insert(0, welcomeComment)
                else:
                    comment = content.contents[0]
                    comment.replace_with(welcomeComment)
                HTML.seek(0)
                HTML.truncate(0)
                HTML.write(content.prettify(formatter=None))

        def addBoard(self):
            link = "index.html"
            categoryName = categoryDict[self.category]

            with open(self.path, "r+", encoding="utf-8") as HTML:
                content = BeautifulSoup(HTML, "html.parser")
                article = content.body.article

                boardString = f"""
                            <a href="{link}" id="return">{categoryName}</a>
                            <img src="../images/asterisk.svg" id="asterisk" alt="" />
                          """

                hasBoard = article.find(id="board")
                if not hasBoard:
                    boardTag = content.new_tag("div", id="board")
                    boardTag.string = boardString
                    article.insert(0, boardTag)
                else:
                    board = article.find(id="board")
                    board.string = boardString

                HTML.seek(0)
                HTML.truncate(0)
                HTML.write(content.prettify(formatter=None))

        def setDate(self):
            with open(self.path, "r+", encoding="utf-8") as HTML:
                content = BeautifulSoup(HTML, "html.parser")
                dateTag = content.find(id="article-header-date")
                dateTag.string = dateTag.string.replace("-", ".")
                # 写入
                HTML.seek(0)
                HTML.truncate(0)
                HTML.write(content.prettify(formatter=None))

        def updateHead(self):
            with open(self.path, "r+", encoding="utf-8") as HTML:
                content = BeautifulSoup(HTML, "html.parser")
                head = content.head
                headTemplate = f"""
                                <meta charset="utf-8" />
                                <meta http-equiv="Content-Language" content="zh-CN" />
                                <meta name="language" content="zh-CN" />
                                <meta name="viewport" content="width=device-width, initial-scale=1.0" />

                                <title>Woodash * {self.title}</title>
                                <meta name="description" content="技术与美学与数字花园" />
                                <meta name="author" content="woodash" />
                                <meta name="date" content="{self.date}" />

                                <meta name="woodash-note" content="{self.note}">
                                <meta name="woodash-tucao" content="{self.tucao}">
                                <meta name="woodash-scene" content="{self.scene}">
                                
                                <link rel="icon" href="../images/favicon.ico" />
                                <link rel="preconnect" href="https://ik.imagekit.io" crossorigin />
                                """
                headTemplate = dedent(headTemplate)
                for style in self.style:
                    headTemplate += f"""{style}"""
                    headTemplate += "\n"
                    
                headTemplate += dedent(f"""
                                <script defer src="../scripts/article/setImageSize.js"></script>
                                """)
                headTemplate = indent(headTemplate, "  ")
                head.clear()
                head.append((headTemplate))
                # 写入
                HTML.seek(0)
                HTML.truncate(0)
                HTML.write(content.prettify(formatter=None))

        def addContents(self):
            with open(self.path, "r+", encoding="utf-8") as HTML:
                content = BeautifulSoup(HTML, "html.parser")
                article = content.body.article

                oldContents = article.find_all(id="索引")
                for oldTag in oldContents:
                    oldTag.extract()

                titles = article.find_all(class_="level2")
                contentsTag = content.new_tag("section")
                contentsTag["id"] = "索引"
                contentsTag["class"] = "level2"

                def turnIntoListItem(_titleTag):
                    name = _titleTag.h2.string.strip()
                    id = _titleTag.get("id")
                    string = f'<li><a href="#{id}">{name}</a></li>'
                    return string

                contentsTag.string = f"""<h2>索引</h2>
                                    <ul>
                                    {"".join(map(turnIntoListItem, titles))}
                                    </ul>"""
                articleHeader = article.header
                articleHeader.insert_after(contentsTag)

                HTML.seek(0)
                HTML.truncate(0)
                HTML.write(content.prettify(formatter=None))

        def addSummary(self):
            with open(self.path, "r+", encoding="utf-8") as HTML:
                content = BeautifulSoup(HTML, "html.parser")
                article = content.body.article
                titles = article.find_all("h2")
                titles = map(lambda x: x.string.strip(), titles)
                ignoreList = ["索引", "生活", "摘录", "网页", "创作", "图像", "结"]
                summary = [title for title in titles if title not in ignoreList]
                self.note = "/".join(summary)

        if self.category != "index":
            setAttrs(self)
            addBoard(self)
            setDate(self)

        if self.category == "weekly":
            if self.title == "半燃其零・钻木求火码后记":
                pass
            else:
                addContents(self)
                addSummary(self)

        setStyle(self)
        addWelcome(self)
        updateHead(self)


def getPages(_category):
    _pages = []
    categoryDir = folder / _category

    for fileName in categoryDir.iterdir():
        # if Path(fileName).suffix != "html":
        # continue
        page = Page()
        page.title = Path(fileName).stem
        page.path = Path(fileName)

        if Path(fileName).stem == "index":
            page.category = "index"
        else:
            page.category = _category
        page.edit()

        ignore = page.category == "index" or not page.note
        if not ignore:
            _pages.append(page)

    _pages.sort(key=lambda x: x.date, reverse=True)

    return _pages


def updateCategoryIndex(_pages, _category):
    article = ""
    for page in _pages:
        newString = f"""
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
        article = "".join([article, newString])
    categoryIndex = Path(f"{_category}/index.html")
    with open(categoryIndex, "r+", encoding="utf-8") as HTML:
        content = BeautifulSoup(HTML, "html.parser")
        header = content.body.main.header

        oldArticles = content.find_all("article")
        for oldArticle in oldArticles:
            oldArticle.extract()

        header.insert_after(BeautifulSoup(dedent(article), "html.parser"))
        HTML.seek(0)
        HTML.truncate(0)
        HTML.write(content.prettify(formatter=None))


def updateMainIndex(_pages):
    mainIndex = Path("index.html")
    article = ""
    for page in _pages:
        newString = f"""
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
        article = "".join([article, newString])
    with open(mainIndex, "r+", encoding="utf-8") as HTML:
        content = BeautifulSoup(HTML, "html.parser")
        target = content.body.main.find(id="column-right")
        target.clear()
        target.append(BeautifulSoup(dedent(article), "html.parser"))
        HTML.seek(0)
        HTML.truncate(0)
        HTML.write(content.prettify(formatter=None))


allPages = []

for category in categorys:
    categoryPages = getPages(category)
    updateCategoryIndex(categoryPages, category)
    allPages.extend(categoryPages)


allPages.sort(key=lambda x: x.date, reverse=True)
updateMainIndex(allPages)
