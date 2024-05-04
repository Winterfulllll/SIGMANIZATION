function registerUser() {
  const userData = {
    username: document.getElementById("username").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
    surname: document.getElementById("surname").value,
    name: document.getElementById("name").value,
    patronymic: document.getElementById("patronymic").value,
  };

  // Регистрация пользователя
  fetch("/api/users", {
    method: "POST",
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data && data.username) {
        // Отправка предпочтений после успешной регистрации
        const username = data.username;
        // Получаем выбранные предпочтения

        const selectedPrefGenres = [];
        const selectedPrefCountries = [];
        const selectedPrefYears = [];

        preferenceCheckboxes.forEach((checkbox) => {
          if (checkbox.checked) {
            switch (checkbox.name) {
              case "preference-genre":
                selectedPrefGenres.push(checkbox.dataset.value);
                break;
              case "preference-country":
                selectedPrefCountries.push(checkbox.dataset.value);
                break;
              case "preference-year":
                selectedPrefYears.push(checkbox.dataset.value);
                break;
            }
          }
        });

        // Создаём массив промисов для отправки предпочтений
        const preferencePromises = [];
        selectedPrefGenres.forEach((genre) =>
          preferencePromises.push(
            sendPreference(username, "GENRE", "MOVIE", genre)
          )
        );
        selectedPrefCountries.forEach((country) =>
          preferencePromises.push(
            sendPreference(username, "COUNTRY", "MOVIE", country)
          )
        );
        selectedPrefYears.forEach((year) =>
          preferencePromises.push(
            sendPreference(username, "YEAR", "MOVIE", year)
          )
        );

        // Отправляем все предпочтения и обрабатываем результат
        Promise.all(preferencePromises)
          .then(() => {
            alert("Пользователь и предпочтения успешно сохранены!");
          })
          .catch((error) => {
            fetch(`/api/users/${username}`, {
              method: "DELETE",
              headers: {
                "Content-Type": "application/json",
                "API-KEY": service_api_key,
              },
            });
            console.error("Ошибка при сохранении предпочтений:", error);
            alert("Произошла ошибка при сохранении предпочтений.");
          });
      } else {
        alert("Произошла ошибка при регистрации.");
      }
    })
    .catch((error) => {
      console.error("Ошибка при регистрации:", error);
    });
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

function loginUser() {
  const loginData = {
    username: document.getElementById("login-username").value,
    password: document.getElementById("login-password").value,
    remember_me: document.getElementById("remember-me").checked,
  };

  fetch("/api/login", {
    method: "POST",
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(loginData),
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      throw new Error("Ошибка авторизации");
    })
    .then((data) => {
      if (data) {
        alert("Вы успешно вошли в систему!");
      } else {
        alert("Неверное имя пользователя или пароль.");
      }
    })
    .catch((error) => {
      alert(error.message);
    });
}

// =============================================================================================================================

// Получаем модальное окно
var modal = document.getElementById("myModal");

// Получаем кнопку, которая открывает модальное окно
var btn = document.getElementById("modalBtn");

// Получаем элемент <span>, который закрывает модальное окно
var span = document.getElementsByClassName("close-button")[0];

// При клике на кнопку открываем модальное окно
btn.onclick = function () {
  modal.style.display = "block";
};

// При клике на <span> (крестик), закрываем модальное окно
span.onclick = function () {
  modal.style.display = "none";
};

// При клике вне модального окна, закрываем его
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

// =============================================================================================================================

// Получаем модальное окно
var modal2 = document.getElementById("myModal2");

// Получаем кнопку, которая открывает модальное окно
var btn2 = document.getElementById("modalBtn2");

// Получаем элемент <span>, который закрывает модальное окно
var span2 = document.getElementsByClassName("close-button2")[0];

// При клике на кнопку открываем модальное окно
btn2.onclick = function () {
  modal2.style.display = "block";
};

// При клике на <span> (крестик), закрываем модальное окно
span2.onclick = function () {
  modal2.style.display = "none";
};

// При клике вне модального окна, закрываем его
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

// Обновлённый обработчик для кнопки "Login"
var loginBtn = document.querySelector(".btn-outline-primary.me-2");
loginBtn.addEventListener("click", function () {
  modal.style.display = "block";
});

// =============================================================================================================================

function createMovieElement(movie) {
  if (!movie || !movie.poster.previewUrl || !movie.name) {
    return null;
  }

  // Создаем контейнер для карточки фильма
  const movieElement = document.createElement("div");
  movieElement.className = "movie-card";
  movieElement.setAttribute("data-id", movie.id);

  // Создаем элемент изображения для постера фильма
  const movieImage = document.createElement("img");
  movieImage.src = movie.poster.previewUrl;
  movieImage.alt = movie.name;
  movieImage.className = "movie-image";

  // Создаем название фильма
  const movieTitle = document.createElement("h3");
  movieTitle.textContent = movie.name;
  movieTitle.className = "movie-title";

  // Объединяем элементы внутри карточки фильма
  movieElement.appendChild(movieImage);
  movieElement.appendChild(movieTitle);

  movieElement.addEventListener("click", () => {
    window.location.href = `/movie/${movie.id}`; // Переходим на страницу фильма
  });

  // Возвращаем готовый элемент
  return movieElement;
}

// =============================================================================================================================

const filterCheckboxes = document.querySelectorAll(
  'input[name="filters-genre"], input[name="filters-country"], input[name="filters-year"], input[name="filters-rating"]'
);

const preferenceCheckboxes = document.querySelectorAll(
  'input[name="preference-genre"], input[name="preference-country"], input[name="preference-year"]'
);

// =============================================================================================================================

let onPage = 5;
let currentPage = 1;

function fetchMoviesByFilters(
  genres = [],
  countries = [],
  years = [],
  ratings = []
) {
  let url = `https://api.kinopoisk.dev/v1.4/movie?page=${currentPage}&limit=${onPage}&selectFields=id&selectFields=name&selectFields=poster&notNullFields=id&notNullFields=name&notNullFields=poster.url`;

  if (genres.length > 0) {
    url += `&genres.name=${genres.join("&genres.name=")}`;
  }

  if (countries.length > 0) {
    url += `&countries.name=${countries.join("&countries.name=")}`;
  }

  if (years.length > 0) {
    url += `&year=${years.join("&year=")}`;
  }

  if (ratings.length > 0) {
    url += `&rating.imdb=${ratings.join("&rating.imdb=")}`;
  }

  fetch(url, {
    method: "GET",
    headers: {
      "X-API-KEY": movies_api_key,
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const movies = data.docs;
      const totalMovies = data.total;

      const moviesContainer = document.getElementById("movies-container");
      moviesContainer.innerHTML = ""; // Очищаем контейнер

      // Добавляем фильмы в контейнер
      movies.forEach((movie) => {
        const movieElement = createMovieElement(movie);
        if (movieElement) {
          moviesContainer.appendChild(movieElement);
        }
      });

      // Получаем кнопки "Предыдущая" и "Следующая"
      const prevButton = document.getElementById("prev");
      const nextButton = document.getElementById("next");

      // Обновляем состояние кнопок
      prevButton.style.display = currentPage === 1 ? "none" : "block";
      nextButton.style.display =
        currentPage * onPage >= totalMovies ? "none" : "block";

      prevButton.removeEventListener("click", handlePrevClick);
      nextButton.removeEventListener("click", handleNextClick);

      prevButton.addEventListener("click", handlePrevClick);
      nextButton.addEventListener("click", handleNextClick);
    })
    .catch((error) => {
      console.error("Ошибка при получении данных:", error);
    });
}

// Обработчик для кнопки "Предыдущая"
function handlePrevClick() {
  currentPage--;
  fetchMoviesAndUpdate();
}

// Обработчик для кнопки "Следующая"
function handleNextClick() {
  currentPage++;
  fetchMoviesAndUpdate();
}

function fetchMoviesAndUpdate() {
  const selectedGenres = [];
  const selectedCountries = [];
  const selectedYears = [];
  const selectedRatings = [];
  filterCheckboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      switch (checkbox.name) {
        case "filters-genre":
          selectedGenres.push(checkbox.dataset.value);
          break;
        case "filters-country":
          selectedCountries.push(checkbox.dataset.value);
          break;
        case "filters-year":
          selectedYears.push(checkbox.dataset.value);
          break;
        case "filters-rating":
          selectedRatings.push(checkbox.dataset.value);
          break;
      }
    }
  });

  fetchMoviesByFilters(
    selectedGenres,
    selectedCountries,
    selectedYears,
    selectedRatings
  );
}

// =============================================================================================================================

let currentPage3 = 1;

function fetchMoviesTop250() {
  fetch(
    `https://api.kinopoisk.dev/v1.4/movie?page=${currentPage3}&limit=${onPage}&lists=top250&selectFields=id&selectFields=name&selectFields=poster&notNullFields=id&notNullFields=name&notNullFields=poster.url`,
    {
      method: "GET",
      headers: {
        "X-API-KEY": movies_api_key,
        "Content-Type": "application/json",
      },
    }
  )
    .then((response) => response.json())
    .then((data) => {
      const movies = data.docs;
      const totalMovies = data.total;

      const moviesContainer = document.getElementById("movies-container-3");
      moviesContainer.innerHTML = ""; // Очищаем контейнер

      // Добавляем фильмы в контейнер
      movies.forEach((movie) => {
        const movieElement = createMovieElement(movie);
        if (movieElement) {
          moviesContainer.appendChild(movieElement);
        }
      });

      // Получаем кнопки "Предыдущая" и "Следующая"
      const prevButton = document.getElementById("prev-3");
      const nextButton = document.getElementById("next-3");

      // Обновляем состояние кнопок
      prevButton.style.display = currentPage3 === 1 ? "none" : "block";
      nextButton.style.display =
        currentPage3 * onPage >= totalMovies ? "none" : "block";

      prevButton.removeEventListener("click", handlePrevClick3);
      nextButton.removeEventListener("click", handleNextClick3);

      prevButton.addEventListener("click", handlePrevClick3);
      nextButton.addEventListener("click", handleNextClick3);
    })
    .catch((error) => {
      console.error("Ошибка при получении данных:", error);
    });
}

// Обработчик для кнопки "Предыдущая"
function handlePrevClick3() {
  currentPage3--;
  fetchMoviesTop250();
}

// Обработчик для кнопки "Следующая"
function handleNextClick3() {
  currentPage3++;
  fetchMoviesTop250();
}

document.addEventListener("DOMContentLoaded", fetchMoviesTop250);

// =============================================================================================================================

filterCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", () => {
    currentPage = 1;
    fetchMoviesAndUpdate();
  });
});

fetchMoviesByFilters();
