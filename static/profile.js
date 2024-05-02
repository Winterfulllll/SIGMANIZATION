function fetchViewedFilms() {
  fetch("api/reviews/" + current_user_username, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "API-KEY": service_api_key,
    },
  })
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
