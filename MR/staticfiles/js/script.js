document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.carousel');
    const cards = document.querySelectorAll('.movie-card');
    const modal = document.getElementById('movieModal');
    const closeButton = modal.querySelector('.close-button');
    let currentIndex = 0;
    const cardWidth = 320; // card width + gap

    // Carousel Navigation
    function updateCarousel() {
        carousel.style.transform = `translateX(${-currentIndex * cardWidth}px)`;
    }

    document.querySelector('.prev-button').addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            updateCarousel();
        }
    });

    document.querySelector('.next-button').addEventListener('click', () => {
        if (currentIndex < cards.length - 3) {
            currentIndex++;
            updateCarousel();
        }
    });

    // Modal Functionality
    cards.forEach(card => {
        card.addEventListener('click', () => {
            // Obtener datos de los atributos data-*
            const movieData = {
                title: card.dataset.movieTitle,
                director: card.dataset.movieDirector,
                cast: card.dataset.movieCast,
                keywords: card.dataset.movieKeywords,
                vote_average: card.dataset.movieVote,
                synopsis: card.dataset.movieSynopsis
            };

            // Actualizar el contenido del modal
            modal.querySelector('.movie-title').textContent = movieData.title;
            modal.querySelector('.movie-director').textContent = movieData.director;
            modal.querySelector('.movie-cast').textContent = movieData.cast;
            modal.querySelector('.movie-keywords').textContent = movieData.keywords;
            modal.querySelector('.movie-vote').textContent = movieData.vote_average;
            modal.querySelector('.movie-synopsis').textContent = movieData.synopsis;

            // Mostrar el modal
            modal.classList.add('active');
        });
    });

    closeButton.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    // Cerrar modal al hacer clic fuera del contenido
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });

    // Control con teclas
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            modal.classList.remove('active');
        }
        if (e.key === 'ArrowLeft') {
            if (currentIndex > 0) {
                currentIndex--;
                updateCarousel();
            }
        }
        if (e.key === 'ArrowRight') {
            if (currentIndex < cards.length - 3) {
                currentIndex++;
                updateCarousel();
            }
        }
    });
});