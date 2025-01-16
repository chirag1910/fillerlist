const setSecondsValue = (value) => {
    document.querySelector(".main p").innerText =
        "Redirecting to main page in " + value + " seconds...";
};

const countdown = (seconds) => {
    setSecondsValue(seconds);

    if (seconds === 0) {
        window.location = "/";
        return;
    }

    seconds -= 1;
    setTimeout(() => countdown(seconds), 1000);
};

countdown(3);
