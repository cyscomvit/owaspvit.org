const html = document.querySelector('html');
const logo = document.querySelector('.valo_logo');
const text = document.querySelector('h1');

html.addEventListener('click', () => {
  valo_logo.style.webkitAnimation = 'none';
  text.style.webkitAnimation = 'none';
  setTimeout(function() {
    valo_logo.style.webkitAnimation = '';
    text.style.webkitAnimation = '';
  }, 10);
});