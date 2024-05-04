const passwordInput = document.getElementById("password");
const repeatPasswordContainer = document.getElementById(
  "repeat-password-container"
);
repeatPasswordContainer.style.display = "none";

// Обработчик события input для поля "Пароль"
passwordInput.addEventListener("input", () => {
  if (passwordInput.value !== "") {
    repeatPasswordContainer.style.display = "block";
  } else {
    repeatPasswordContainer.style.display = "none";
  }
});

// =============================================================================================================================

