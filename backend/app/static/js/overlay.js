const overlayContainer = document.querySelector('.overlay-container');
const closeBtn = document.querySelector('.overlay-close-btn');
const overlayVideo = document.querySelector('.overlay-video iframe');

closeBtn.addEventListener('click', function () {
    overlayContainer.style.display = 'none';
    overlayVideo.src = "";
});