import { switchForm } from "./utils.js";

const buttonsContainer = document.getElementById("buttons-container");
const [...buttons] = buttonsContainer.children;

buttons.forEach((button) =>
  button.addEventListener("click", function () {
    switchForm(this, buttonsContainer);
  })
);

if (document.getElementById("login-btn").hasAttribute("data-login")) {
  buttons[0].click();
}
