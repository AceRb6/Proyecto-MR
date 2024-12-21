document.addEventListener('DOMContentLoaded', function() {
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
  
    // Redireccionar a la página de recomendaciones después de la carga
    setTimeout(() => {
      window.location.href = '/recommender/'; // URL de la página de recomendaciones
    }, 55000); // Tiempo de redirección en milisegundos

    function randomText(){
        var text = ("!@#$%^*()")
        letters =text[Math.floor(Math.random() * text.length)];
        return letters;
    }
    
    function rain() {
        let cloud = document.querySelector('.cloud');
        let e = document.createElement('div');
        e.classList.add('drop');
        cloud.appendChild(e);
    
        let left = Math.floor(Math.random() * 5)
        let size = Math.random() * 1.5;
        let duration = Math.random() *1;
    
        e.innerText = randomText();
        e.style.left = left + 'px';
        e.style.fontSize = 0.5+size +'em';
        e.style.animationDuration = 1+duration+'s';
    
          setTimeout(function(){
          cloud.removeChild(e)
          },2000)
    }
    
    setInterval(function(){
        rain()
    },20);
  });