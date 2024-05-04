const movie = JSON.parse(movie_json).docs[0];

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

// Получаем элементы формы
const viewedCheckbox = document.getElementById("viewed");
const reviewText = document.getElementById("reviewText");
const ratingInput = document.getElementById("rating");
const submitReviewButton = document.getElementById("submitReview");

// Обработчик события клика на кнопку "Отправить отзыв"
submitReviewButton.addEventListener("click", () => {
  const isViewed = viewedCheckbox.checked;
  const review = reviewText.value.trim();
  const rating = ratingInput.value.trim();

  // Отправляем данные отзыва на сервер (пример)
  fetch(`/api/reviews/${current_user_username}`, {
    method: "POST",
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      item_id: movie.id,
      viewed: isViewed,
      item_category: "MOVIE",
      ...(review && { review: review }),
      ...(rating && { rating: parseInt(rating, 10) }),
    }),
  })
    .then((response) => {
      if (response.ok) {
        // Запрос успешен
        return response.json(); // Получаем JSON-ответ сервера
      } else {
        // Ошибка на сервере
        throw new Error(
          "Ошибка при отправке отзыва. Код ошибки: " + response.status
        );
      }
    })
    .then((data) => {
      // Обработка успешного ответа
      console.log("Отзыв успешно отправлен:", data);
      alert("Спасибо за ваш отзыв!");

      const reviewContainer = document.getElementById("review"); // Замени 'reviewContainer' на ID контейнера
      reviewContainer.style.display = "none";
    })
    .catch((error) => {
      // Обработка ошибок
      console.error("Ошибка при отправке отзыва:", error);
      alert("Произошла ошибка при отправке отзыва.");
    });
});
