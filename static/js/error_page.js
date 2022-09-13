var seconds = 3;

const countdown = () => {
    seconds -= 1;
    if (seconds === 0){
        window.location="/";
    }
    document.querySelector(".error-section p").innerText="Redirecting to main page in " + seconds + " seconds...";
}

setInterval(countdown, 1000);
