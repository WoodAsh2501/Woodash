let imgs = document.querySelectorAll("figure img");
let sumRatio = 0;
for (let i = 0; i < imgs.length; i++) {
    const img = imgs[i];
    let ratio = img.naturalWidth / img.naturalHeight;
    sumRatio += ratio;
}
// 页面第一次加载好的时候重设图片宽度
setImageSize();
// 窗口大小变更时再次重设图片宽度
window.addEventListener('resize', setImageSize);

function setImageSize() {
    let article = document.querySelector("article");
    let height = article.offsetWidth / sumRatio;
    
    for (let i = 0; i < imgs.length; i++) {
        const img = imgs[i];
        img.style.height = height + 'px';
    }

    console.log("已重设图片尺寸")
}