document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  
    // Navbar effect on scroll
    let prevScrollpos = window.pageYOffset;
    window.onscroll = function() {
      const currentScrollPos = window.pageYOffset;
      const navbar = document.querySelector('.content');
  
      if (prevScrollpos > currentScrollPos) {
        navbar.style.top = '0';
      } else {
        navbar.style.top = '-80px';
      }
  
      prevScrollpos = currentScrollPos;
    };
  
    // Automatic carousel setup
    function setupCarousel() {
      const carousel = document.querySelector('.carousel');
      if (!carousel) return;
  
      // Limit duplicated items
      const items = carousel.querySelectorAll('.movie-card');
      const itemsToClone = Math.min(items.length, 10);
  
      for (let i = 0; i < itemsToClone; i++) {
        const clone = items[i].cloneNode(true);
        carousel.appendChild(clone);
      }
    }
  
    setupCarousel();
  
    const syncPointer = ({ x: pointerX, y: pointerY }) => {
      const x = pointerX.toFixed(2)
      const y = pointerY.toFixed(2)
      const xp = (pointerX / window.innerWidth).toFixed(2)
      const yp = (pointerY / window.innerHeight).toFixed(2)
      document.documentElement.style.setProperty('--x', x)
      document.documentElement.style.setProperty('--xp', xp)
      document.documentElement.style.setProperty('--y', y)
      document.documentElement.style.setProperty('--yp', yp)
    }
  
    document.body.addEventListener('pointermove', syncPointer)
  
    const genreButtons = document.querySelectorAll('.genre-btn');
  
    genreButtons.forEach(button => {
      button.addEventListener('click', (e) => {
        const genre = e.target.dataset.genre;
        updateMovieCarousel(genre);
      });
    });
  
    function updateMovieCarousel(genre) {
      // Depuración: muestra el género seleccionado
      console.log('Género seleccionado:', genre);
  
      // Actualizar texto del género
      const genreText = document.querySelector('.genre-section p');
      if (genreText) {
        genreText.textContent = `Género seleccionado: ${genre}`;
      }
  
      // Actualizar estado de los botones
      genreButtons.forEach((btn) => {
        btn.classList.remove('active');
        if (btn.dataset.genre === genre) {
          btn.classList.add('active');
        }
      });
  
      // Llamar a la función para cargar películas
      fetchMoviesByGenre(genre);
    }
  
    async function fetchMoviesByGenre(genre) {
      try {
        // Construir URL con el género
        const url = `/genres/?genre=${encodeURIComponent(genre)}`;
  
        // Hacer solicitud AJAX
        const response = await fetch(url, {
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        });
  
        // Verificar si la respuesta es exitosa
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
  
        // Parsear respuesta JSON
        const movies = await response.json();
  
        // Depuración: mostrar películas recibidas
        console.log('Películas recibidas:', movies);
  
        // Renderizar películas
        renderMovieCarousel(movies, genre);
      } catch (error) {
        console.error('Error al cargar películas:', error);
  
        // Mostrar mensaje de error
        const carouselContainer = document.querySelector('.movie-carousel');
        if (carouselContainer) {
          carouselContainer.innerHTML = `
            <div class="error-message">
              No se pudieron cargar las películas. Error: ${error.message}
            </div>
          `;
        }
      }
    }
  
    function renderMovieCarousel(movies, genre) {
      // Verificar si el contenedor existe
      const carouselContainer = document.querySelector('.movie-carousel');
      if (!carouselContainer) {
        console.error('Contenedor de carrusel no encontrado');
        return;
      }
  
      // Limpiar contenedor
      carouselContainer.innerHTML = '';
  
      // Verificar si hay películas
      if (!movies || movies.length === 0) {
        carouselContainer.innerHTML = `
          <div class="no-movies-message">
            No se encontraron películas para el género ${genre}
          </div>
        `;
        return;
      }
  
      // Renderizar películas
      movies.forEach(movie => {
        const movieCard = document.createElement('div');
        movieCard.classList.add('movie-card');
        movieCard.dataset.genre = genre;
  
        // Crear contenido de la tarjeta de película
        movieCard.innerHTML = `
          <img src="${movie.imagen}" alt="${movie.title}">
          <h3>${movie.title}</h3>
          <p>Calificacion: ${movie.vote_average}</p>
          <p>${movie.sipnosis}</p>
        `;
  
        carouselContainer.appendChild(movieCard);
      });
    }
  
    // Agregar evento de mouse para mover el carrusel
    const carouselContainer = document.querySelector('.movie-carousel');
    if (carouselContainer) {
      let isDown = false;
      let startX;
      let scrollLeft;
  
      carouselContainer.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.clientX - carouselContainer.offsetLeft;
        scrollLeft = carouselContainer.scrollLeft;
      });
  
      carouselContainer.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const newX = e.clientX - carouselContainer.offsetLeft;
        carouselContainer.scrollLeft = scrollLeft + (startX - newX);
      });
  
      carouselContainer.addEventListener('mouseup', () => {
        isDown = false;
      });
  
      carouselContainer.addEventListener('wheel', (e) => {
        e.preventDefault();
        carouselContainer.scrollLeft += e.deltaX;
      });
    }
  });