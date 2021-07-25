const buttonsContainer = document.getElementById("buttons-container");
const registerBtn = document.getElementById("register-btn");
const registerForm = document.getElementById("register");
const loginBtn = document.getElementById("login-btn");
const loginForm = document.getElementById("login");

function switchForm(buttonElement, toLogin = true) {
    const buttonValue = buttonElement.value;

    buttonsContainer.style.transform = `translateX(${getTranslateAmount(buttonValue)})`;

    if (buttonElement.value === "login") {
        loginForm.classList.toggle("hidden");
    } else if (buttonElement.value === "register") {
        registerForm.classList.toggle("hidden");
    }

    // Timeout so the form isn't hidden immediately. Makes the transition smoother
    setTimeout(() => {
        registerBtn.classList.toggle("hidden");
        loginBtn.classList.toggle("hidden");

        toLogin ? registerForm.classList.toggle("hidden") : loginForm.classList.toggle("hidden");
    }, 200);
}

/**
 * Determines the value to be used in a translate CSS function, depending on which button is being clicked.
 * @param {string} buttonValue The button element's value attribute.
 * @returns The value that will be used in a translate CSS function.
 */
function getTranslateAmount(buttonValue) {
    if (buttonValue === "login") {
        return "40vw";
    } else if (buttonValue === "register") {
        return "0";
    }
}
