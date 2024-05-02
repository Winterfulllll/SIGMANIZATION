        function registerUser() {
            const userData = {
                username: document.getElementById('username').value,
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                surname: document.getElementById('surname').value,
                name: document.getElementById('name').value,
                patronymic: document.getElementById('patronymic').value
            };

            fetch('/api/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'API-KEY': service_api_key,
                },
                body: JSON.stringify(userData)
            })
            .then(response => response.json())
            .then(data => {
                if (data && data.username) {
                    alert('Пользователь успешно зарегистрирован!');
                } else {
                    alert('Произошла ошибка при регистрации.');
                }
            })
            .catch(error => {
                console.error('Ошибка при регистрации:', error);
            });
        }


        function loginUser() {
            const loginData = {
                username: document.getElementById('login-username').value,
                password: document.getElementById('login-password').value,
                remember_me: document.getElementById('remember-me').checked
            };

            fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'API-KEY': service_api_key,
                },
                body: JSON.stringify(loginData)
            })
            .then(response => {
                if(response.ok) {
                    return response.json();
                }
                throw new Error('Ошибка авторизации');
            })
            .then(data => {
                if (data) {
                    alert('Вы успешно вошли в систему!');
                } else {
                    alert('Неверное имя пользователя или пароль.');
                }
            })
            .catch(error => {
                alert(error.message);
            });
        }

        // Получаем модальное окно
        var modal = document.getElementById("myModal");

        // Получаем кнопку, которая открывает модальное окно
        var btn = document.getElementById("modalBtn");

        // Получаем элемент <span>, который закрывает модальное окно
        var span = document.getElementsByClassName("close-button")[0];

        // При клике на кнопку открываем модальное окно
        btn.onclick = function() {
            modal.style.display = "block";
        }

        // При клике на <span> (крестик), закрываем модальное окно
        span.onclick = function() {
            modal.style.display = "none";
        }

        // При клике вне модального окна, закрываем его
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

        // Получаем модальное окно
        var modal2 = document.getElementById("myModal2");

        // Получаем кнопку, которая открывает модальное окно
        var btn2 = document.getElementById("modalBtn2");

        // Получаем элемент <span>, который закрывает модальное окно
        var span2 = document.getElementsByClassName("close-button2")[0];

        // При клике на кнопку открываем модальное окно
        btn2.onclick = function() {
            modal2.style.display = "block";
        }

        // При клике на <span> (крестик), закрываем модальное окно
        span2.onclick = function() {
            modal2.style.display = "none";
        }

        // При клике вне модального окна, закрываем его
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

        // Обновлённый обработчик для кнопки "Login"
        var loginBtn = document.querySelector('.btn-outline-primary.me-2');
        loginBtn.addEventListener('click', function() {
            modal.style.display = "block";
        });

        let currentPage = 1;
        let onPage = 5;

        function fetchMovies() {
            fetch(`https://api.kinopoisk.dev/v1.4/movie?page=${currentPage}&limit=${onPage}&selectFields=id&selectFields=name&selectFields=poster&notNullFields=id&notNullFields=name&notNullFields=poster.url`, {
                method: 'GET',
                headers: {
                    'X-API-KEY': movies_api_key,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                const movies = data.docs;
                const totalMovies = data.total;

                const moviesContainer = document.getElementById('movies-container');
                moviesContainer.innerHTML = ''; // Очищаем контейнер

                // Добавляем фильмы в контейнер
                movies.forEach(movie => {
                    const movieElement = createMovieElement(movie);
                    if (movieElement) {
                        moviesContainer.appendChild(movieElement);
                    }
                });

                // Получаем кнопки "Предыдущая" и "Следующая"
                const prevButton = document.getElementById('prev');
                const nextButton = document.getElementById('next');

                // Обновляем состояние кнопок
                prevButton.style.display = (currentPage === 1) ? 'none' : 'block';
                nextButton.disabled = currentPage * onPage >= totalMovies;

                prevButton.removeEventListener('click', handlePrevClick); // Удаляем предыдущий обработчик
                nextButton.removeEventListener('click', handleNextClick); // Удаляем предыдущий обработчик

                prevButton.addEventListener('click', handlePrevClick); // Добавляем новый обработчик
                nextButton.addEventListener('click', handleNextClick); // Добавляем новый обработчик
            })
            .catch(error => {
                console.error('Ошибка при получении данных:', error);
            });
        }

        function fetchMoviesByFilters(genres, countries, years, ratings) {
            let url = `https://api.kinopoisk.dev/v1.4/movie?page=${currentPage}&limit=${onPage}&selectFields=id&selectFields=name&selectFields=poster&notNullFields=id&notNullFields=name&notNullFields=poster.url`;

            if (genres.length > 0) {
                url += `&genres.name=${genres.join('&genres.name=')}`;
            }

            if (countries.length > 0) {
                url += `&countries.name=${countries.join('&countries.name=')}`;
            }

            if (years.length > 0) {
                url += `&year=${years.join('&year=')}`;
            }

            if (ratings.length > 0) {
                url += `&rating.imdb=${ratings.join('&rating.imdb=')}`;
            }

            fetch(url, {method: 'GET', headers: {
                    'X-API-KEY': movies_api_key,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                const movies = data.docs;
                const totalMovies = data.total;
                const moviesContainer = document.getElementById('movies-container-2');
                moviesContainer.innerHTML = '';

                movies.forEach(movie => {
                    const movieElement = createMovieElement(movie);
                    if (movieElement) {
                        moviesContainer.appendChild(movieElement);
                    }
                });

                // Создаем элементы для пагинации
                const paginationContainer = document.createElement('div');
                paginationContainer.className = 'pagination';

                const prevButton = document.createElement('button');
                prevButton.textContent = '<< Предыдущая';
                prevButton.disabled = currentPage === 1;
                prevButton.addEventListener('click', () => {
                    currentPage--;
                    fetchMovies();
                });

                const nextButton = document.createElement('button');
                nextButton.textContent = 'Следующая >>';
                nextButton.disabled = currentPage * onPage >= totalMovies;
                nextButton.addEventListener('click', () => {
                    currentPage++;
                    fetchMovies();
                });

                paginationContainer.appendChild(prevButton);
                paginationContainer.appendChild(nextButton);

                moviesContainer.appendChild(paginationContainer);
            })
            .catch(error => {
                console.error('Ошибка при получении данных:', error);
            });
            }

        // Обработчик для всех чекбоксов
        const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
        allCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const selectedGenres = [];
            const selectedCountries = [];
            const selectedYears = [];
            const selectedRatings = [];
            allCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                switch (checkbox.name) {
                case 'genre': selectedGenres.push(checkbox.dataset.value); break;
                case 'country': selectedCountries.push(checkbox.dataset.value); break;
                case 'year': selectedYears.push(checkbox.dataset.value); break;
                case 'rating': selectedRatings.push(checkbox.dataset.value); break;
                }
            }
        });
            fetchMoviesByFilters(selectedGenres, selectedCountries, selectedYears, selectedRatings);
        });
        });

        // Обработчик для кнопки "Предыдущая"
        function handlePrevClick() {
            currentPage--;
            fetchMovies();
        }

        // Обработчик для кнопки "Следующая"
        function handleNextClick() {
            currentPage++;
            fetchMovies();
        }

        function createMovieElement(movie) {
            if (!movie || !movie.poster.previewUrl || !movie.name) {
                return null;
            }

            // Создаем контейнер для карточки фильма
            const movieElement = document.createElement('div');
            movieElement.className = 'movie-card';

            // Создаем элемент изображения для постера фильма
            const movieImage = document.createElement('img');
            movieImage.src = movie.poster.previewUrl;
            movieImage.alt = movie.name;
            movieImage.className = 'movie-image';

            // Создаем название фильма
            const movieTitle = document.createElement('h3');
            movieTitle.textContent = movie.name;
            movieTitle.className = 'movie-title';

            // Объединяем элементы внутри карточки фильма
            movieElement.appendChild(movieImage);
            movieElement.appendChild(movieTitle);

            // Возвращаем готовый элемент
            return movieElement;
        }

        document.addEventListener('DOMContentLoaded', fetchMovies);