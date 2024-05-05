const movie = JSON.parse(movie_json).docs[0];

const reviewContainer = document.getElementById("review");
const reviewHeading = document.getElementById("reviewHeading");
const deleteReview = document.getElementById("deleteReview");

deleteReview.style.display = "none";

// Проверяем, авторизован ли пользователь
if (current_user_username !== "None") {
  reviewContainer.style.display = "block";
} else {
  reviewContainer.style.display = "none";
}

let existingReviewId = null; // Переменная для хранения ID существующего отзыва
let method = null;
let url = null;
fetchUserReview();

// Функция для получения отзыва пользователя
function fetchUserReview() {
  fetch(`/api/reviews/${current_user_username}`, {
    method: "GET",
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // Проверяем, есть ли отзыв с текущим movie_id
      const review = data.find((item) => item.item_id === movie.id);
      if (review) {
        existingReviewId = review.id;
        viewedCheckbox.checked = review.viewed;
        reviewText.value = review.review || "";
        ratingInput.value = review.rating || 5;
      }

      method = existingReviewId ? "PATCH" : "POST";
      url = existingReviewId
        ? `/api/reviews?id=${existingReviewId}`
        : `/api/reviews/${current_user_username}`;
      reviewHeading.textContent = existingReviewId
        ? "Редактировать отзыв"
        : "Оставить отзыв";
      deleteReview.style.display = existingReviewId ? "block" : "none";
    })
    .catch((error) => {
      console.error("Ошибка при получении отзыва:", error);
    });
}

// =============================================================================================================================

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

  // Отправляем данные отзыва на сервер
  fetch(url, {
    method: method,
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      item_id: movie.id,
      viewed: isViewed || false,
      item_category: "MOVIE",
      ...(review && { review: review }),
      ...(rating && { rating: parseInt(rating, 10) }),
    }),
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error(
          "Ошибка при отправке отзыва. Код ошибки: " + response.status
        );
      }
    })
    .then((data) => {
      console.log("Отзыв успешно отправлен:", data);

      if (!existingReviewId) {
        alert("Спасибо за ваш отзыв!");
        existingReviewId = data.id; // Получаем ID нового отзыва
        reviewHeading.textContent = "Редактировать отзыв"; // Изменяем заголовок
        method = "PATCH";
        url = `/api/reviews?id=${existingReviewId}`;
        deleteReview.style.display = "block";
      } else {
        alert("Отзыв был успешно отредактирован");
      }

      // const reviewContainer = document.getElementById("review");
      // reviewContainer.style.display = "none";
    })
    .catch((error) => {
      console.error("Ошибка при отправке отзыва:", error);
      alert("Произошла ошибка при отправке отзыва.");
    });
});

deleteReview.addEventListener("click", () => {
  fetch(`/api/reviews?id=${existingReviewId}`, {
    method: "DELETE",
    headers: {
      "API-KEY": service_api_key,
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (response.ok) {
        console.log("Отзыв успешно удален");
        alert("Ваш отзыв был удален.");

        // Обновляем состояние и UI
        existingReviewId = null;
        method = "POST";
        url = `/api/reviews/${current_user_username}`;
        reviewHeading.textContent = "Оставить отзыв";

        // Очищаем форму отзыва
        viewedCheckbox.checked = false;
        reviewText.value = "";
        ratingInput.value = 5;

        deleteReview.style.display = "none";
      } else {
        throw new Error(
          "Ошибка при удалении отзыва. Код ошибки: " + response.status
        );
      }
    })
    .catch((error) => {
      console.error("Ошибка при удалении отзыва:", error);
      alert("Произошла ошибка при удалении отзыва.");
    });
});
