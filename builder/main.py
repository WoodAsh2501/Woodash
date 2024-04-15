from globalVar import *
from updateIndex import updateCategoryIndex, updateMainIndex
import page

allPages = []
for category in categorys:
    categoryPages = list(map(page.formatPage, page.getPages(category, directory)))
    categoryPages.sort(key=lambda x: x.date, reverse=True)
    updateCategoryIndex(categoryPages, category)
    allPages.extend(categoryPages)

allPages.sort(key=lambda x: x.date, reverse=True)
updateMainIndex(allPages)
