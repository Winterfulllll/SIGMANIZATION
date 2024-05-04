const movie = JSON.parse(movie_json).docs[0]

document.addEventListener("DOMContentLoaded", function () {
  if (movie) {
    document.getElementById("movieTitle").textContent =
      movie.name || "Название неизвестно";
    if (movie.poster && movie.poster.url) {
      const poster = document.getElementById("moviePoster");
      poster.src = movie.poster.url;
      poster.style.display = "block";
    }
    document.getElementById("movieDescription").innerHTML =
      movie.description || "Описание отсутствует";
  } else {
    document.getElementById("movieTitle").textContent = "Фильм не найден";
    document.getElementById("movieDescription").textContent = "";
  }
});
