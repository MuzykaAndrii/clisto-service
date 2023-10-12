const overlayContainer = document.querySelector('.overlay-container');
const closeBtn = document.querySelector('.overlay-close-btn');

closeBtn.addEventListener('click', function () {
    overlayContainer.style.display = 'none';
});