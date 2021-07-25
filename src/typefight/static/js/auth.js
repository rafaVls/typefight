const buttonsContainer = document.getElementById("buttons-container");
const registerBtn = document.getElementById("register-btn");
const registerForm = document.getElementById("register");
const loginBtn = document.getElementById("login-btn");
const loginForm = document.getElementById("login");

/**
 * Handles switching from the "login" form to the "register" form and vice-versa.
 * @param {HTMLButtonElement} buttonElement The button element that's calling this function.
 */
function switchForm(buttonElement) {
    const buttonValue = buttonElement.value;

    buttonsContainer.style.transform = `translateX(${getTranslateAmount(buttonValue)})`;
    toggleClasses(buttonValue);
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

/**
 * Determine which elements' classes will be "toggled", depending on buttonValue.
 * @param {string} buttonValue The button element's value attribute.
 */
function toggleClasses(buttonValue) {
    const className = "hidden";
    const loginValue = buttonValue === "login";
    const registerValue = buttonValue === "register";

    loginValue && loginForm.classList.toggle(className);
    registerValue && registerForm.classList.toggle(className);

    // Timeout so the form isn't hidden immediately. Makes the transition smoother
    setTimeout(() => {
        registerBtn.classList.toggle(className);
        loginBtn.classList.toggle(className);

        loginValue && registerForm.classList.toggle(className);
        registerValue && loginForm.classList.toggle(className);
    }, 200);
}
