const overlayContainer = document.querySelector('.overlay-container');
const closeBtn = document.querySelector('.overlay-close-btn');
const overlayVideo = document.querySelector('.overlay-video iframe');
const overlayDescription = document.querySelector('.overlay-text');
const overlayTitle = document.querySelector('.overlay-title');


closeBtn.addEventListener('click', function () {
    overlayContainer.style.display = 'none';
    overlayVideo.src = "";
});

function YtUrlToEmbed(ytUrl) {
    // Check if the provided URL is a valid YouTube URL
    var regex = /(?:https:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([A-Za-z0-9_-]+)/;
    var match = ytUrl.match(regex);
  
    if (match) {
      // If it's a valid URL, construct the embedded URL
      var videoId = match[1];
      var embedUrl = 'https://www.youtube.com/embed/' + videoId;
      return embedUrl;
    } else {
      // If the URL doesn't match the expected pattern, return null or an error message
      return null;
    }
  }

$(".subcat-item").on("click", function () {
    $(overlayVideo).attr("src", YtUrlToEmbed($(this).attr("videoUrl")));
    $(overlayDescription).html($(this).attr("description"));
    $(overlayContainer).css('display', 'block');
    $(overlayTitle).html($(this).find(".subcat-header").html());
});