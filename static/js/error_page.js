var seconds = 3;

const countdown = () => {
    if (seconds === 0) {
        window.location = "/";
    }

    document.querySelector(".main p").innerText =
        "Redirecting to main page in " + seconds + " seconds...";

    seconds -= 1;
};

setInterval(countdown, 1000);
