document.addEventListener('DOMContentLoaded', () => {
  const message1 = document.getElementById('message1');
  const message2 = document.getElementById('message2');
  const movieCardsContainer = document.getElementById('movie-cards');

  message1.style.display = 'block';

  setTimeout(function() {
    message1.style.display = 'none';
    message2.style.display = 'block';
  }, 5000);

  setTimeout(function() {
    message2.style.display = 'none';
    loadMovies();
  }, 10000);

  let currentPage = 1;
  const moviesPerPage = 12;
  let selectedMovies = [];
  let numSelectedMovies = 0;

  // Función para cargar películas
  async function loadMovies() {
    try {
      const response = await fetch(`/advanced/json/?page=${currentPage}`);
      const data = await response.json();

      console.log(data);

      data.forEach(movie => {
        const movieCard = createMovieCard(movie);
        movieCardsContainer.appendChild(movieCard);
      });

      currentPage++;
    } catch (error) {
      console.error('Error cargando películas:', error);
    }
  }

  // Función para cargar más películas
  async function loadMoreMovies() {
    console.log('Cargando más películas...');
    try {
      const response = await fetch(`/advanced/json/?page=${currentPage}`);
      const data = await response.json();

      console.log('Películas cargadas:', data);

      data.forEach(movie => {
        const movieCard = createMovieCard(movie);
        movieCardsContainer.appendChild(movieCard);
      });

      currentPage++;
    } catch (error) {
      console.error('Error cargando más películas:', error);
    }
  }

  // Agregar evento de desplazamiento
  window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY + window.innerHeight;
    const containerHeight = movieCardsContainer.offsetHeight;

    if (scrollPosition >= containerHeight) {
      loadMoreMovies();
    }
  });

  // Crear tarjeta de película
  function createMovieCard(movie) {
    console.log(movie); // agrega esto para verificar el contenido
    const movieCard = document.createElement('div');
    console.log(movieCard); 
    movieCard.classList.add('movie-card');
    movieCard.dataset.movieId = movie.id;

    movieCard.innerHTML = `
      <div class="movie-card-inner">
        <div class="movie-card-front" style="background-image: url(${movie.imagen})"></div>
        <div class="movie-card-back">
          <h3>${movie.title}</h3>
          <input type="number" id="rating" min="1" max="10" step="0.1" placeholder="Calificación">
        </div>
      </div>
    `;

    // Evento de selección de película
    movieCard.addEventListener('click', (event) => {
      if (event.target.id === 'rating') {
        return;
      }

      movieCard.classList.toggle('selected');

      const movieId = movieCard.dataset.movieId;
      if (movieCard.classList.contains('selected')) {
        selectedMovies.push(movieId);
        numSelectedMovies++;
      } else {
        selectedMovies = selectedMovies.filter(id => id !== movieId);
        numSelectedMovies--;
      }

      // Actualiza el botón de guardar selección
      const saveSelectionBtn = document.getElementById('save-selection-btn');
      if (numSelectedMovies >= 3) {
        saveSelectionBtn.disabled = false;
      } else {
        saveSelectionBtn.disabled = true;
      }
    });

    // Evento de cambio de calificación
    const ratingInput = movieCard.querySelector('#rating');
    ratingInput.addEventListener('change', (event) => {
      const rating = parseFloat(event.target.value);
      if (!isNaN(rating) && rating >= 1 && rating <= 10) {
        saveRating(movie.id, rating);
      }
    });

    return movieCard;
  }

  // Evento de guardar selección
  const saveSelectionBtn = document.getElementById('save-selection-btn');
  saveSelectionBtn.disabled = true;
  saveSelectionBtn.addEventListener('click', async () => {
    if (numSelectedMovies < 3) {
      alert('Por favor, selecciona al menos 3 películas.');
      return;
    }

    try {
      const ratings = [];
      selectedMovies.forEach((movieId) => {
        const movieCard = document.querySelector(`.movie-card[data-movie-id="${movieId}"]`);
        const ratingInput = movieCard.querySelector('#rating');
        const rating = parseFloat(ratingInput.value);
        if (!isNaN(rating) && rating >= 1 && rating <= 10) {
          ratings.push({ movie_id: movieId, rating });
        }
      });

      const movieIds = selectedMovies.map(movieId => movieId);
      const ratingsData = ratings.map(rating => rating.rating);

      const data = {
        'movies[]': movieIds.map(id => `movies[]=${id}`).join('&'),
        'ratings[]': ratingsData.map(rating => `ratings[]=${rating}`).join('&')
      };

      const response = await fetch('/save-selected-movies/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: `${data['movies[]']}&${data['ratings[]']}`
      });

      if (response.ok) {
        // Redirigir o mostrar mensaje de éxito
        window.location.href = '/preparing/';
      } else {
        const errorData = await response.json();
        alert(errorData.message || 'Error al guardar las películas');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });

  // Función para obtener cookie CSRF (necesaria para Django)
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Función para guardar calificación
  function saveRating(movieId, rating) {
    // Código para guardar calificación
  }
});