const buttonsContainer = document.getElementById("buttons-container");
const registerBtn = document.getElementById("register-btn");
const registerForm = document.getElementById("register");
const loginBtn = document.getElementById("login-btn");
const loginForm = document.getElementById("login");

function login() {
    buttonsContainer.style.transform = "translateX(40vw)";

    registerBtn.classList.remove("hidden");
    registerForm.classList.add("hidden");
    loginForm.classList.remove("hidden");
    loginBtn.classList.add("hidden");
}

function register() {
    buttonsContainer.style.transform = "translateX(0)";

    registerForm.classList.remove("hidden");
    registerBtn.classList.add("hidden");
    loginBtn.classList.remove("hidden");
    loginForm.classList.add("hidden");
}