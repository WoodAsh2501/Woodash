const shapeController = document.getElementById("shapeController");

const smoothController = document.getElementById("smoothController");
const fluentController = document.getElementById("fluentController");

const fireTarget = document.getElementById("fire");
let totalHeight = 50;
let totalWidth = 128;
// 火焰根部高度
let bottomHeight = totalHeight * 0.1;

let smoothFactor = 0.5;
let fluentFactor = 0.7;

smoothController.addEventListener("input", () => {
    smoothFactor = smoothController.value;
})
fluentController.addEventListener("input", () => {
    fluentFactor = fluentController.value;
})


let center1 = 0.5;
let radius1 = 0.2;

let center2 = 0.5;
let radius2 = 0.3;

let flameArray = Array.from({ length: totalHeight }, () => Array(totalWidth).fill(" "));
let flameData = Array(totalWidth);
let previousFlameData = Array(totalWidth).fill(0);


const loop = setInterval(refresh, 250, fireTarget, flameArray);

function refresh(DOMtarget, asciiArray) {
    randomFlame(flameArray);
    flameData = fluentizeAnimation(previousFlameData, flameData);
    drawFlame(flameArray, smoothFlame(flameData));
    previousFlameData = flameData.slice();
    let asciiFlame = Array(totalHeight)
    for (i = 0; i < asciiArray.length; i++) {
        asciiFlame[i] = asciiArray[i].join("")
    }
    DOMtarget.innerHTML = asciiFlame.join("\n");
}

function randomFlame(asciiArray) {
    let step = Math.random() * 0.05;
    if (Math.random() > 0.5) {
        center1 += step;
        center1 %= 1;
    } else {
        center1 -= step;
        center1 %= 1;
    }

    if (Math.random() > 0.5) {
        center2 += step;
        center2 %= 1;
    } else {
        center2 -= step;
        center2 %= 1;
    }

    for (xPos = 0; xPos < totalWidth; xPos++) {
        let heightScaler = 0;
        heightScaler += subFlame(0.5, 0.5, 0.4);
        heightScaler += subFlame(center1, radius1, 0.4);
        heightScaler += subFlame(center2, radius2, 0.2);

        let height = randomInt(bottomHeight, totalHeight, heightScaler);
        
        flameData[xPos] = height;
    }

    function randomInt(min, max, scaler) {
        let height = Math.floor(Math.random() * (max - min) + min);
        height = Math.ceil(height * scaler);
        return height;
    }

    function subFlame(centerIN, radiusIn, value) {
        let center = totalWidth * centerIN;
        let radius = totalWidth *  radiusIn;

        let distanceToCenter = Math.abs(xPos - center);
        let x;

        if (distanceToCenter <= radius) {
            x = distanceToCenter / radius;
        } else {
            x = 1;
        }

        scalerOut = value * (1 - x ** 2) / (1 + (x / radius) ** 2);
        return scalerOut;
    }
}

function smoothFlame(flameDataIn) {
    let smoothed = flameDataIn.slice();
    for (xPos = 1; xPos < totalWidth - 1; xPos++) {
        let height = smoothed[xPos];
        let heightAverage = (smoothed[xPos - 1] + smoothed[xPos] + smoothed[xPos + 1]) / 3;
        smoothed[xPos] = height + (heightAverage - height) * smoothFactor;
    }
    return smoothed;
}

function fluentizeAnimation(previousFlameDataInput, flameDataInput) {
    fluentized = Array(totalWidth);
    for (xPos = 0; xPos < totalWidth; xPos++) {
        previousHeight = previousFlameDataInput[xPos];
        currentHeight = flameDataInput[xPos];
        deltaHeight = currentHeight - previousHeight;

        fluentized[xPos] = previousHeight + deltaHeight * (1-fluentFactor);
        // console.log(previousHeight, currentHeight, fluentized[xPos]);
    }
    return fluentized;
}

function drawFlame(asciiArray, flameDataIn) {
    for (xPos = 0; xPos < totalWidth; xPos++) {
        for (yPos = totalHeight - 1; yPos > 0; yPos--) {
            if (totalHeight - 1 - yPos < flameDataIn[xPos]) {
                asciiArray[yPos][xPos] = "#";
            } else {
                asciiArray[yPos][xPos] = " ";
            }
        }
    }
}

