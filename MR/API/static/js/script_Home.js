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
});