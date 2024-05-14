let viewedMovieIds = [];
const moviesContainer = document.getElementById("movies-container");

async function fetchViewedMovieIds() {
  try {
    const response = await fetch(`api/reviews/${current_user_username}`, {
      method: "GET",
      headers: {
        "API-KEY": service_api_key,
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    viewedMovieIds = data
      .filter((review) => review.viewed === true)
      .map((review) => review.item_id);

    if (viewedMovieIds.length > 0) {
      fetchViewedFilmsWithPagination();
    } else {
      moviesContainer.innerHTML = "<p>Здесь пока пусто! =(</p>";
    }
  } catch (error) {
    console.error("Ошибка при получении просмотренных фильмов:", error);
  }
}

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

let onPage = 5;
let currentPage = 1;

async function fetchViewedFilmsWithPagination() {
  try {
    const startIndex = (currentPage - 1) * onPage;
    const endIndex = startIndex + onPage;
    const pageMovieIds = viewedMovieIds.slice(startIndex, endIndex);

    if (pageMovieIds.length > 0) {
      const url = `https://api.kinopoisk.dev/v1.4/movie?id=${pageMovieIds.join(
        "&id="
      )}&selectFields=id&selectFields=name&selectFields=poster&notNullFields=id&notNullFields=name&notNullFields=poster.url`;

      const response = await fetch(url, {
        method: "GET",
        headers: {
          "X-API-KEY": movies_api_key,
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();
      moviesContainer.innerHTML = "";

      data.docs.forEach((movieData) => {
        const movieElement = createMovieElement(movieData);
        if (movieElement) {
          moviesContainer.appendChild(movieElement);
        }
      });
    }

    updatePaginationButtons();
  } catch (error) {
    console.error("Ошибка при получении данных:", error);
  }
}

function updatePaginationButtons() {
  const prevButton = document.getElementById("prev");
  const nextButton = document.getElementById("next");

  prevButton.style.display = currentPage === 1 ? "none" : "block";
  nextButton.style.display =
    currentPage * onPage >= viewedMovieIds.length ? "none" : "block";

  prevButton.removeEventListener("click", handlePrevClick);
  nextButton.removeEventListener("click", handleNextClick);

  prevButton.addEventListener("click", handlePrevClick);
  nextButton.addEventListener("click", handleNextClick);
}

function handlePrevClick() {
  currentPage--;
  fetchViewedFilmsWithPagination();
}

function handleNextClick() {
  currentPage++;
  fetchViewedFilmsWithPagination();
}

// =============================================================================================================================

document.addEventListener("DOMContentLoaded", fetchViewedMovieIds);
