const newPasswordInput = document.getElementById("new-password");
const repeatPasswordContainer = document.getElementById(
  "repeat-password-container"
);
repeatPasswordContainer.style.display = "none";

// Обработчик события input для поля "Пароль"
newPasswordInput.addEventListener("input", () => {
  if (newPasswordInput.value !== "") {
    repeatPasswordContainer.style.display = "block";
  } else {
    repeatPasswordContainer.style.display = "none";
  }
});

// =============================================================================================================================

fetchUserInfoAndPreferences();

function fetchUserInfoAndPreferences() {
  // Получаем информацию о пользователе
  fetch(`/api/users/${current_user_username}`, {
    method: "GET",
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((userData) => {
      // Заполняем текстовые поля
      document.getElementById("username").value = userData.username;
      document.getElementById("email").value = userData.email;
      document.getElementById("surname").value = userData.surname;
      document.getElementById("name").value = userData.name;
      document.getElementById("patronymic").value = userData.patronymic;

      // Получаем предпочтения пользователя
      return fetch(`/api/preferences/${current_user_username}`, {
        method: "GET",
        headers: {
          "API-KEY": service_api_key,
          "Content-Type": "application/json",
        },
      });
    })
    .then((response) => response.json())
    .then((preferenceData) => {
      // Заполняем чекбоксы предпочтений
      const preferenceCheckboxes = document.querySelectorAll(
        'input[name="preference-genre"], input[name="preference-country"], input[name="preference-year"]'
      );
      setPreferenceCheckboxes(preferenceCheckboxes, preferenceData);
    })
    .catch((error) => {
      console.error("Ошибка при получении данных:", error);
    });
}

// Вспомогательная функция для установки состояния чекбоксов
function setPreferenceCheckboxes(checkboxes, preferences) {
  checkboxes.forEach((checkbox) => {
    const type = checkbox.name.split("-")[1].toUpperCase();
    const value = checkbox.dataset.value;

    // Проверяем наличие предпочтений нужного типа и категории
    const preferenceMatch = preferences.find(
      (p) => p.type === type && p.type_value === value
    );
    checkbox.checked = preferenceMatch !== undefined;
  });
}

// =============================================================================================================================

const preferenceCheckboxes = document.querySelectorAll(
  'input[name="preference-genre"], input[name="preference-country"], input[name="preference-year"]'
);

function resetPreferenceCheckboxes() {
  preferenceCheckboxes.forEach((checkbox) => {
    checkbox.checked = false;
  });
}

// Привязываем функцию к кнопке
const resetButton = document.getElementById("delete-preferences");
resetButton.addEventListener("click", resetPreferenceCheckboxes);

const changeButton = document.getElementById("change-profile");
changeButton.addEventListener("click", handleProfileChange);

// =============================================================================================================================

async function handleProfileChange() {
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const newPassword = document.getElementById("new-password").value;
  const repeatPassword = document.getElementById("repeat-password").value;
  const surname = document.getElementById("surname").value;
  const name = document.getElementById("name").value;
  const patronymic = document.getElementById("patronymic").value;
  const currentPassword = document.getElementById("password").value;

  // Проверка пароля и повтора пароля
  if (newPassword !== repeatPassword) {
    alert("Новый пароль и повтор пароля не совпадают!");
    return;
  }

  try {
    // Проверка пароля
    await checkPassword(current_user_username, currentPassword);

    // Сбор предпочтений
    const preferencesData = collectPreferences();

    // Формирование данных пользователя
    const newUserData = {
      username,
      email,
      password: newPassword || currentPassword,
      ...(surname && { surname }),
      ...(name && { name }),
      ...(patronymic && { patronymic }),
    };

    // Обновление данных пользователя
    await updateUser(current_user_username, newUserData);

    // Удаление старых и добавление новых предпочтений
    await updatePreferences(username, preferencesData);

    alert("Данные профиля и предпочтения успешно обновлены!");
    current_user_username = username; // Обновляем имя пользователя
    location.reload();
  } catch (error) {
    console.error("Ошибка при обновлении данных:", error);
    alert(error.message);
  }
}

function sendPreference(username, type, category, typeValue) {
  const preferenceData = {
    type: type,
    category: category,
    type_value: typeValue,
  };

  return fetch(`/api/preferences/${username}`, {
    method: "POST",
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(preferenceData),
  });
}

async function checkPassword(username, password) {
  const passwordCheckResponse = await fetch("/api/password_check", {
    method: "POST",
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  if (!passwordCheckResponse.ok) {
    // Обработка ошибок ответа сервера (например, 400, 401)
    const errorData = await passwordCheckResponse.json();
    throw new Error(`Ошибка проверки пароля: ${errorData.message}`);
  }

  const passwordCheckData = await passwordCheckResponse.json();

  if (!passwordCheckData) {
    throw new Error("Ошибка: Неверный текущий пароль.");
  }
}

function collectPreferences() {
  const selectedGenres = [];
  const selectedCountries = [];
  const selectedYears = [];

  preferenceCheckboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      switch (checkbox.name) {
        case "preference-genre":
          selectedGenres.push(checkbox.dataset.value);
          break;
        case "preference-country":
          selectedCountries.push(checkbox.dataset.value);
          break;
        case "preference-year":
          selectedYears.push(checkbox.dataset.value);
          break;
      }
    }
  });

  return {
    genres: selectedGenres,
    countries: selectedCountries,
    years: selectedYears,
  };
}

async function updateUser(username, userData) {
  const response = await fetch(`/api/users/${username}`, {
    method: "PUT",
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    // Обработка ошибок ответа сервера
    if (response.status === 400) {
      const data = await response.json();
      throw new Error(`Ошибка: Некорректные данные. ${data.message}`);
    } else if (response.status === 401) {
      throw new Error("Ошибка: Неверный пароль.");
    } else {
      throw new Error("Произошла ошибка при обновлении данных.");
    }
  }

  return response;
}

async function updatePreferences(username, preferencesData) {
  // Удаление всех существующих предпочтений
  await fetch(`/api/preferences/${current_user_username}`, {
    method: "DELETE",
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
    },
  });

  // Добавление новых предпочтений поштучно
  const preferencePromises = [];
  preferencesData.genres.forEach((genre) =>
    preferencePromises.push(sendPreference(username, "GENRE", "MOVIE", genre))
  );
  preferencesData.countries.forEach((country) =>
    preferencePromises.push(
      sendPreference(username, "COUNTRY", "MOVIE", country)
    )
  );
  preferencesData.years.forEach((year) =>
    preferencePromises.push(sendPreference(username, "YEAR", "MOVIE", year))
  );

  await Promise.all(preferencePromises);
}
