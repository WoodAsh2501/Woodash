document.addEventListener("DOMContentLoaded", makeContents);

function makeContents() {
    console.log("makeContents!");
    const subTitles = document.querySelectorAll("h2");
    const articleHeader = document.querySelector(".article-header");
    const article = document.querySelector("article");
    
    let contents = document.createElement("section");
    contents.setAttribute("id", "索引");
    contents.setAttribute("class", "level2");
    
    article.insertBefore(contents, articleHeader.nextElementSibling)
    const title = document.createElement("h2");
    title.innerHTML = "索引"
    contents.appendChild(title)
    
    const list = document.createElement("ul");
    contents.appendChild(list);
    
    for (let i = 0; i < subTitles.length; i++) {
        const listNode = document.createElement("li");
        const anchor = document.createElement("a");
        anchor.innerHTML = subTitles[i].innerHTML;
        anchor.setAttribute("href", "#" + subTitles[i].innerHTML);
        listNode.appendChild(anchor);
        list.appendChild(listNode);
    }
}

