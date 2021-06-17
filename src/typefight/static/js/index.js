const timer = document.getElementById("timer");
const startBtn = document.getElementById("start-btn");

let minutes = 0;
let seconds = 0;
let start = 0;
let timerInterval;

function startGame() {
    start = new Date().getTime();
    startBtn.innerText = "Restart";
    startBtn.setAttribute("onclick", "resetGame()");

    timerInterval = setInterval(() => {
        seconds++;
        if (seconds === 60) {
            seconds = 0;
            minutes++;
        }

        timer.innerText =
            (minutes < 10 ? ("0" + minutes) : minutes) + ":" +
            (seconds < 10 ? ("0" + seconds) : seconds);
    }, 1000)
}

function resetGame() {
    clearInterval(timerInterval);
    console.log(((new Date().getTime() - start) / 1000).toFixed(2));

    startBtn.setAttribute("onclick", "startGame()");
    startBtn.innerText = "Start";
    timer.innerText = "00:00";

    seconds = 0;
    minutes = 0;
    start = 0;
}