document.addEventListener('DOMContentLoaded', function() {
  const items = document.querySelectorAll('.slide .item');
  let currentIndex = 0;

  function showSlide(index) {
      // Remover clase active de todos los items
      items.forEach(item => item.classList.remove('active'));
      
      // Añadir clase active al item actual
      items[index].classList.add('active');
  }

  // Botón siguiente
  document.querySelector('.next').addEventListener('click', () => {
      currentIndex = (currentIndex + 1) % items.length;
      showSlide(currentIndex);
  });

  // Botón anterior
  document.querySelector('.prev').addEventListener('click', () => {
      currentIndex = (currentIndex - 1 + items.length) % items.length;
      showSlide(currentIndex);
  });

  // Autoplay opcional
  setInterval(() => {
      currentIndex = (currentIndex + 1) % items.length;
      showSlide(currentIndex);
  }, 10000); // Cambia cada 5 segundos
});