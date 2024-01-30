// 如果图片的load事件能正确触发的话就不用废这么大力气轮询了，感觉幽默

const imgs = document.querySelectorAll("figure img");
let sumRatio = 0;
let imgsLoaded = false;

// 加载完成时重设尺寸
let timer = setInterval(checkImagesLoaded, 500);

// 窗口大小变更时重设图片尺寸
window.addEventListener('resize', setImageSize);

function checkImagesLoaded() {
    let flag = true;
    for (let i = 0; i < imgs.length; i++) {
        const img = imgs[i];
        if (!img.complete) {
            flag = false;
            break;
        };
        let ratio = img.naturalWidth / img.naturalHeight;
        sumRatio += ratio;
    }
    imgsLoaded = (flag) ? true : false;  
    console.log(sumRatio);

    if (imgsLoaded) {
        setImageSize();
        clearInterval(timer);
    }
}

function setImageSize() {
    // 如果加载错误就不重设尺寸
    if (sumRatio === 0) {
        return
    }
    let article = document.querySelector("article");
    let height = article.offsetWidth / sumRatio;
    // console.log(article.offsetWidth, sumRatio, height);

    for (let i = 0; i < imgs.length; i++) {
        const img = imgs[i];
        img.style.height = height + 'px';
        img.style.width = "auto";
    }
}