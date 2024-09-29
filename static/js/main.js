const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

setTimeout(function () {
    $(".message-container").fadeOut("slow");
}, 3000);