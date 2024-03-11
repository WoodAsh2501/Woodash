// 如果图片的load事件能正确触发的话就不用废这么大力气轮询了，感觉幽默
const imgsDiv = document.querySelectorAll(".imgs");

const imgsFlex = document.querySelector(".imgs");
imgsFlex.style.width = 'fit-content';

for (let i = 0; i < imgsDiv.length; i++) {
    const imgsPerLine = imgsDiv[i].querySelectorAll("img");
    // 加载完成时重设尺寸

    let timerToCheckLoaded;
    timerToCheckLoaded = setInterval(() => {
        let loaded = checkImagesLoaded(imgsPerLine);
        if (loaded) {
            let sumRatio = countRatio(imgsPerLine);
            setImageSize(imgsPerLine, sumRatio);
            clearInterval(timerToCheckLoaded);
        }
    }, 500);

    // 窗口大小变更时重设图片尺寸
    window.addEventListener('resize', () => {
        let sumRatio = countRatio(imgs);
        setImageSize(imgsPerLine, sumRatio)
    });
}

function checkImagesLoaded(imgs) {
    let flag = true;
    for (let i = 0; i < imgs.length; i++) {
        const img = imgs[i];
        if (!img.complete) {
            flag = false;
            break;
        };
    }
    loaded = (flag) ? true : false;
    // console.log(sumRatio);
    return loaded;
}

function countRatio(imgs) {
    let sumRatio = 0;
    for (let i = 0; i < imgs.length; i++) {
        const img = imgs[i];
        let ratio = img.naturalWidth / img.naturalHeight;
        sumRatio += ratio;
    }
    return sumRatio;
}

function setImageSize(imgs, ratio) {
    // 如果加载错误就不重设尺寸
    if (ratio === 0) {
        return
    }
    let article = document.querySelector("article");
    let height = article.offsetWidth / ratio;
    console.log(article.offsetWidth, ratio, height);

    const header = document.querySelector(".page-header");
    let contentHeight = 0.9 * (window.innerHeight - header.offsetHeight);

    // console.log(contentHeight);

    for (let i = 0; i < imgs.length; i++) {
        const img = imgs[i];
        img.style.height = 'min(' + contentHeight + 'px,' + height + 'px)';
        img.style.width = "auto";
    }
    console.log("重设图片尺寸成功！")
}