const fireContainer = document.getElementById("fire");

const canvas = document.createElement("canvas");
canvas.width = 128;
canvas.height = 64;

const ctx = canvas.getContext("2d");
let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
let dataArray = imageData.data;

let char = ".:-=+*#%@";
let flames = [];

const mapRange = (x, originMin, originMax, targetMin, targetMax) => 
                 (x - originMin) / (originMax - originMin) * (targetMax - targetMin) + targetMin;

const lerp = (x, a, b) => (b - a) * x + a;

const createFlame = (x, w, h, s=1) => ({
    xPos: x,
    width: w,
    // height: Math.floor(h * mapRange(Math.random(), 0, 1, 0.9, 1.1)),
    height: h,
    swing: s,
    tick: Math.floor(100 * Math.random()) / 100,
})

const drawFlame = function(flame){
    let output = "";
    // requestAnimationFrame(drawFlame);
    flame.tick += 0.01;
    if (flame.tick > 1) {
        flame.tick--;
    };
    
    for (let i = 0, n= canvas.width * canvas.height; i<n; i++) {
        let x = i % canvas.width;
        let y = canvas.height - Math.ceil(i / canvas.width);
        
        let ratioFromBottom = 0;
        if (y <= flame.height) {
            ratioFromBottom = mapRange(y, 0, flame.height, 1, 0);
        }
        // 调节周期、相位
        let _x = (ratioFromBottom + flame.tick) * 2 * Math.PI *
                 mapRange(Math.random(), 0, 1, 0.95, 1.05);
        // 火体宽度flameBodyWidth，保持底部静止
        let flameBodyWidth = (1-ratioFromBottom) * flame.swing * flame.width * (Math.sin(_x));
        let thinner = flame.width * ratioFromBottom;
        // let thinner = 20;
        
        if (x > flame.xPos + flameBodyWidth - thinner/2 &&
            x < flame.xPos + flameBodyWidth + thinner/2 &&
            y <= flame.height) {
            output += 1;
        }}
    return output;
}

const ignite = function(){
    for (let x = 0; x < canvas.width; x++) {
        if (Math.random() > 0.6) {
        let distanceToCenter = Math.abs(x - canvas.width/2);
        let ratioToCenter = 1-distanceToCenter/(canvas.width/2)
        // 形状函数
        let _x = mapRange((ratioToCenter ** 1) / (1 + (ratioToCenter) ** 2), 0, 1, 0.8, 1)
        // let _x = 0;
        let _w = mapRange(Math.random(), 0, 1, 0.8, 1);
            flames.push(createFlame(x, 32*_w, 32*_x, 0.1))
        }
    }
}

const burnNow = function(){
    let flameData = Array(canvas.width * canvas.height).fill(0);
    for (let i = 0; i < flames.length; i++) {
        let eachFlameData = drawFlame(flames[i])
        for (let j = 0; j < canvas.width * canvas.height; j++) {
            flameData[j] = +flameData[j] + +eachFlameData[j];
        }
    }

    let ascii = "";

    for (let i = 0; i < canvas.width * canvas.height; i++) {
        let index = mapRange(flameData[i], 0, 50, 0, char.length);
        console.log(flameData[i])

            ascii += flameData[i]
    }

    let asciiArray = Array.from(ascii);

    for (let i = canvas.width; i < canvas.width * (canvas.height); i += canvas.width+1) {
        asciiArray.splice(i, 0, "</div><div>");
    }
    console.log(asciiArray)
    asciiArray.splice(0, 0, "<div>");
    asciiArray.push("</div>");

    ascii = asciiArray.join("");

    fireContainer.innerHTML = ascii;

    // requestAnimationFrame(burnNow);
}

// drawFlame(flame0);
ignite();
burnNow();