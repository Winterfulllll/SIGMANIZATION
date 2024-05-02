function fetchViewedFilms() {
  fetch("api/reviews/" + current_user_username, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "API-KEY": service_api_key,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const movieIds = data.map((review) => review.item_id); // Получаем список ID фильмов
      const moviesContainer = document.getElementById("movies-container");
      moviesContainer.innerHTML = ""; // Очищаем контейнер

      // Для каждого ID выполняем запрос в Kinopoisk API
      movieIds.forEach((movieId) => {
        fetch(
          `https://api.kinopoisk.dev/v1.4/movie/${movieId}?selectFields=id&selectFields=name&selectFields=poster¬NullFields=id¬NullFields=name¬NullFields=poster.url`,
          {
            method: "GET",
            headers: {
              "X-API-KEY": movies_api_key,
              "Content-Type": "application/json",
            },
          }
        )
          .then((response) => response.json())
          .then((movieData) => {
            const movieElement = createMovieElement(movieData);
            if (movieElement) {
              moviesContainer.appendChild(movieElement);
            }
          })
          .catch((error) => {
            console.error("Ошибка при получении данных фильма:", error);
          });
      });
    })
    .catch((error) => {
      console.error("Ошибка при получении просмотренных фильмов:", error);
    });
}

function createMovieElement(movie) {
  if (!movie || !movie.poster.previewUrl || !movie.name) {
    return null;
  }

  // Создаем контейнер для карточки фильма
  const movieElement = document.createElement("div");
  movieElement.className = "movie-card";

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

  // Возвращаем готовый элемент
  return movieElement;
}
