document.addEventListener('DOMContentLoaded', function() {
    // Efecto de scroll suave para los enlaces de navegación
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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

    // Efecto de navbar al hacer scroll
    let prevScrollpos = window.pageYOffset;
    window.onscroll = function() {
        const currentScrollPos = window.pageYOffset;
        const navbar = document.querySelector('.navbar');
        
        if (prevScrollpos > currentScrollPos) {
            navbar.style.top = "0";
        } else {
            navbar.style.top = "-80px";
        }
        
        if (currentScrollPos > 100) {
            navbar.style.backgroundColor = "rgba(255, 255, 255, 0.95)";
        } else {
            navbar.style.backgroundColor = "rgba(255, 255, 255, 0.9)";
        }
        
        prevScrollpos = currentScrollPos;
    };
});


// Configuración del carrusel automático
function setupCarousel() {
    const carousel = document.querySelector('.carousel');
    if (!carousel) return;

    // Duplicar elementos para scroll infinito
    const items = carousel.querySelectorAll('.movie-card');
    items.forEach(item => {
        const clone = item.cloneNode(true);
        carousel.appendChild(clone);
    });
}

// Configuración de particles.js para los botones
function setupParticles() {
    const particlesConfig = {
        particles: {
            number: {
                value: 50,
                density: {
                    enable: true,
                    value_area: 800
                }
            },
            color: {
                value: "#0088cc"
            },
            opacity: {
                value: 0.5,
                random: false,
                animation: {
                    enable: false
                }
            },
            size: {
                value: 3,
                random: true
            },
            line_linked: {
                enable: true,
                distance: 150,
                color: "#0088cc",
                opacity: 0.4,
                width: 1
            },
            move: {
                enable: true,
                speed: 6
            }
        },
        interactivity: {
            detect_on: "canvas",
            events: {
                onhover: {
                    enable: true,
                    mode: "repulse"
                }
            }
        }
    };

    // Inicializar particles.js en cada botón
    document.querySelectorAll('.feature-btn').forEach((btn, index) => {
        const particlesContainer = document.createElement('div');
        particlesContainer.id = `particles-${index}`;
        particlesContainer.className = 'particles-js';
        btn.insertBefore(particlesContainer, btn.firstChild);
        particlesJS(`particles-${index}`, particlesConfig);
    });
}

// Evento cuando el DOM está cargado
document.addEventListener('DOMContentLoaded', function() {
    setupCarousel();
    setupParticles();

    // Añadir efectos de hover a los botones de características
    document.querySelectorAll('.feature-btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });

        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
});