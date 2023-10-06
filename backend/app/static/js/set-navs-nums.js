window.addEventListener('DOMContentLoaded', function() {
    var liElements = document.querySelectorAll('.side-nav li');
    liElements.forEach(function(li, index) {
        var position = (index + 1).toString().padStart(2, '0');

        li.setAttribute('data-before', position)
    });
});