const registerBtn = document.getElementById("register-btn");
const registerForm = document.getElementById("register");
const loginBtn = document.getElementById("login-btn");
const loginForm = document.getElementById("login");

/**
 * Handles switching from the "login" form to the "register" form and vice-versa.
 * @param {HTMLButtonElement} buttonElement The button element that's calling this function.
 * @param {HTMLElement} elementToMove The element to move to the left or right.
 */
function switchForm(buttonElement, elementToMove) {
    const buttonValue = buttonElement.value;

    elementToMove.style.transform = `translateX(${getTranslateAmount(buttonValue)})`;
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

    loginValue && toggleClass(loginForm);
    registerValue && toggleClass(registerForm);

    // Timeout so the form isn't hidden immediately. Makes the transition smoother
    setTimeout(() => {
        toggleClass(registerBtn);
        toggleClass(loginBtn);

        loginValue && toggleClass(registerForm);
        registerValue && toggleClass(loginForm);
    }, 200);
}

/**
 * Toggles className from element's classList, removing it if it's present,
 * adding it if it's not.
 * @param {HTMLElement} element The element which class we want to toggle.
 * @param {string} className The class name or value which we want to toggle on/off. Default = "hidden"
 */
function toggleClass(element, className = "hidden") {
    element.classList.toggle(className);
}

export { switchForm };