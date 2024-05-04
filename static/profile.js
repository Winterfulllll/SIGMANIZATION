function fetchViewedFilms() {
  fetch("api/reviews/" + current_user_username, {
    method: "POST",
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
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
          `https://api.kinopoisk.dev/v1.4/movie/${movieId}?selectFields=id&selectFields=name&selectFields=poster&notNullFields=id&notNullFields=name&notNullFields=poster.url`,
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
