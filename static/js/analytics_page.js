const dragLeft = document.querySelector(".drag-left");
const dragRight = document.querySelector(".drag-right");
const range = document.querySelector(".range");
const container = document.querySelector(".range-container");
const totalElem = document.querySelector("#custom-range-total");

var touchDevice =
    "ontouchstart" in window ||
    navigator.maxTouchPoints > 0 ||
    navigator.msMaxTouchPoints > 0;

var draggingLeft = false;
var draggingRight = false;

container.addEventListener(touchDevice ? "touchstart" : "mousedown", (e) => {
    // e.preventDefault();
    const relMouseX =
        (touchDevice ? e.changedTouches[0].pageX : e.pageX) -
        container.getBoundingClientRect().left;
    const leftDist = Math.abs(relMouseX - range.offsetLeft);
    const rightDist = Math.abs(
        relMouseX - (range.offsetLeft + range.offsetWidth)
    );

    if (leftDist < rightDist) {
        draggingLeft = true;
    } else {
        draggingRight = true;
    }
});

document.addEventListener(touchDevice ? "touchmove" : "mousemove", (e) => {
    // e.preventDefault();

    if (draggingLeft) {
        const relMouseX =
            (touchDevice ? e.changedTouches[0].pageX : e.pageX) -
            container.getBoundingClientRect().left;
        const rangeLeft = Math.floor(relMouseX);
        const rangeRight = Math.ceil(range.offsetLeft + range.offsetWidth);
        const contWidth = container.offsetWidth;

        if (rangeRight - rangeLeft >= contWidth / 20 && rangeLeft >= 0) {
            range.style.left = rangeLeft + "px";
            range.style.width = rangeRight - rangeLeft + "px";
        }
    }

    if (draggingRight) {
        const relMouseX =
            (touchDevice ? e.changedTouches[0].pageX : e.pageX) -
            container.getBoundingClientRect().left;
        const rangeLeft = Math.floor(range.offsetLeft);
        const rangeRight = Math.ceil(relMouseX);
        const contWidth = container.offsetWidth;

        if (
            rangeRight - rangeLeft >= contWidth / 20 &&
            rangeRight <= contWidth
        ) {
            range.style.width = rangeRight - rangeLeft + "px";
        }
    }
});

document.addEventListener(touchDevice ? "touchend" : "mouseup", (e) => {
    // e.preventDefault();
    draggingRight = false;
    draggingLeft = false;
});

window.addEventListener("resize", () => {
    range.style.left = 0;
    range.style.width = container.offsetWidth + "px";
});

const setCustomCount = (total) => {
    totalElem.innerText = total;
};
