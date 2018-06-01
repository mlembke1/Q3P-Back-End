$(document).ready(() => {
      $(".dropdown-trigger").dropdown()

      // ANIMATION FOR HOMEPAGE LOAD
      $('.loader').fadeOut(2000)

      // SIGNUP / LOGIN POPOUT FUNCTIONALITY
      $('.collapsible').collapsible()
      if (window.location.hash === '#login-collapsible') {
        $('#login-collapsible').trigger('click')
      } else if (window.location.hash === '#signup-collapsible') {
        $('#signup-collapsible').trigger('click')
      }

      // Typing Effect
      var i = 0;
      var txt = 'A JOURNALING APPLICATION.'; /* The text */
      var speed = 40; /* The speed/duration of the effect in milliseconds */

      function typeWriter() {
        if (i < txt.length) {
          document.getElementById("typing").innerHTML += txt.charAt(i);
          i++;
          setTimeout(typeWriter, speed);
        }
      }
      setTimeout(() => typeWriter(), 1000)

      
})
