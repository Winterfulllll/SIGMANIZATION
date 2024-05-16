const searchButton = document.getElementById("search-button");
const searchInput = document.getElementById("search-input");
searchButton.addEventListener("click", fetchMoviesBySearch);

fetchMoviesBySearch();

function fetchMoviesBySearch() {
  const query = searchInput.value;

  // Проверяем, пустой ли запрос
  const url = query
    ? `https://api.kinopoisk.dev/v1.4/movie/search?limit=21&query=${query}`
    : "https://api.kinopoisk.dev/v1.4/movie?limit=21&&lists=top250";

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
      const moviesContainer = document.getElementById(
        "search-movies-container"
      );
      moviesContainer.innerHTML = ""; // Очищаем контейнер

      // Добавляем фильмы в контейнер
      movies.forEach((movie) => {
        const movieElement = createMovieElement(movie);
        if (movieElement) {
          moviesContainer.appendChild(movieElement);
        }
      });
    })
    .catch((error) => {
      console.error("Ошибка при получении данных:", error);
    });
}

// =====================================================================

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
