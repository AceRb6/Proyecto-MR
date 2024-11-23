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