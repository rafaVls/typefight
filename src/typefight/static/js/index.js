const game = document.getElementById("game");
const timer = document.getElementById("timer");
const startBtn = document.getElementById("start-btn");
const quoteElement = document.getElementById("quote");
const typedValueElement = document.getElementById("typed-value");
const typedValueContainerElement = document.getElementById("typed-value-container");
typedValueElement.value = "";

// Getting all css custom properties
const styles = getComputedStyle(document.documentElement);

let words = [];
let wordIndex = 0;

let minutes = 0;
let seconds = 0;
let start = 0;
let timerInterval;

async function startGame() {
    const quote = await getQuote();
    start = new Date().getTime();

    timer.innerText = "00:00";
    startBtn.innerText = "Restart";
    startBtn.setAttribute("onclick", "resetGame()");

    typedValueElement.addEventListener("input", gameManager);
    typedValueElement.removeAttribute("tabindex");
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

    typedValueElement.setAttribute("tabindex", "-1");
    startBtn.setAttribute("onclick", "startGame()");
    startBtn.innerText = "Start";
    startBtn.focus();

    seconds = 0;
    minutes = 0;
    start = 0;
}

function gameManager(e) {
    const currentWord = words[wordIndex];
    const typedValue = typedValueElement.value;

    if (typedValue === currentWord && wordIndex === words.length - 1) {
        finishGame();
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

function finishGame() {
    clearInterval(timerInterval);
    console.log(((new Date().getTime() - start) / 1000).toFixed(2));

    createHighscoresTable(game);

    startBtn.remove();
    quoteElement.remove();
    typedValueContainerElement.remove();

    timer.style.color = styles.getPropertyValue("--color-text-accent");
    typedValueElement.removeEventListener("input", gameManager);
}

async function getQuote() {
    const res = await fetch("/quote");
    const { quote } = await res.json();

    return quote;
}

async function getHighscores() {
    const res = await fetch("/highscores");
    const highscores = await res.json();

    return highscores;
}

async function createHighscoresTable(containerElement) {
    const highscores = await getHighscores();
    const scoresContainer = document.createElement("table");
    const headers = `
        <thead>
            <th>Highscores</th>
            <th>Name</th>
            <th>Country</th>
        </thead>
        <tbody></tbody>`;

    // can't do highscores.map here because it appends a weird ","
    // after every <tr>, since it returns an array.
    let highscoresData = "";
    for (const score of highscores) {
        const values = `
            <td>${score.score}</td>
            <td>${score.player_name}</td>
            <td>${score.country}</td>`;

        highscoresData += `<tr>${values}</tr>`;
    }

    scoresContainer.innerHTML = headers;
    scoresContainer.lastElementChild.innerHTML = highscoresData;
    scoresContainer.setAttribute("id", "scores-container");

    containerElement.appendChild(scoresContainer);
}