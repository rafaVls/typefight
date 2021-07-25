const buttonsContainer = document.getElementById("buttons-container");
const registerBtn = document.getElementById("register-btn");
const registerForm = document.getElementById("register");
const loginBtn = document.getElementById("login-btn");
const loginForm = document.getElementById("login");

function switchForm(buttonElement, toLogin = true) {
    const translateXAmount = toLogin ? "40vw" : "0";
    buttonsContainer.style.transform = `translateX(${translateXAmount})`;

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
