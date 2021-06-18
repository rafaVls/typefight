const timer = document.getElementById("timer");
const startBtn = document.getElementById("start-btn");
const quoteElement = document.getElementById("quote");
const typedValueElement = document.getElementById("typed-value");

const quote = 'When you have eliminated the impossible, whatever remains, however improbable, must be the truth.';
let words = [];
let wordIndex = 0;

let minutes = 0;
let seconds = 0;
let start = 0;
let timerInterval;

function startGame() {
    start = new Date().getTime();
    timer.innerText = "00:00";
    startBtn.innerText = "Restart";
    startBtn.setAttribute("onclick", "resetGame()");

    typedValueElement.addEventListener("input", gameManager);
    words = quote.split(' ');
    wordIndex = 0;

    const spanWords = words.map(word => `<span>${word} </span>`)
    quoteElement.innerHTML = spanWords.join('');
    quoteElement.childNodes[0].className = "highlight";
    typedValueElement.value = "";
    typedValueElement.focus();

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

    seconds = 0;
    minutes = 0;
    start = 0;
}

function gameManager(e) {
    const currentWord = words[wordIndex];
    const typedValue = typedValueElement.value;

    if (typedValue === currentWord && wordIndex === words.length - 1) {
        resetGame();
        startBtn.focus();
        typedValueElement.remove();
        typedValueElement.removeEventListener("input", gameManager);
    } else if (typedValue.endsWith(" ") && typedValue.trim() === currentWord) {
        typedValueElement.value = "";
        wordIndex++;

        for (const wordElement of quoteElement.childNodes) {
            wordElement.className = "";
        }
        quoteElement.childNodes[wordIndex].className = "highlight";
    } else if (currentWord.startsWith(typedValue)) {
        typedValueElement.className = "";
    }
}