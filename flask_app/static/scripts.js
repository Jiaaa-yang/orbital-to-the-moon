// Utility function to get random integer between min (inclusive) and max (exclusive)
function randInt(min, max) {
    return Math.floor(Math.random() * (max - min) ) + min;
}

// Store cursor position
var mouseX = 200;
var mouseY = 200;
$(document).mousemove(function (event) {
    mouseX = event.pageX;
    mouseY = event.pageY;
})

// Add loading animation for search
$(document).ready(function() {
    $("#search-form").submit(function (event) {
        form = this;
        event.preventDefault();
        $("#analyse-button").addClass("hide");
        $("#loading-button").removeClass("hide");

        setTimeout(function () {
            form.submit();
        }, 100)
    })
})

// Add loading text for clicking of favourited stock
$(".favourite-stocks").click(function (event) {
    link = this.href;
    event.preventDefault();
    $("#loading-text").removeClass('hide');
    $("#main-content").addClass('hide');

    setTimeout(function () {
        window.location.href = link;
    }, 100)
})

$(function() {
    $(".flex-item").click(function (event) {
        $(".flex-item").removeClass("show");
        $(this).addClass("show");
    })
})

// AJAX scripts for displaying sample classification result in AI page
$("#text-classifier-demo form").submit(function(event) {
    event.preventDefault();
    // Check whether it is the general sentiment or financial sentiment form
    var formType = this.id;
    var textInput;
    if (formType == 'general-sentiment') {
        textInput = $('#vader-input').val()
    } else {
        textInput = $('#linearsvc-input').val()
    }

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $(`#${formType} .demo-result`).html(this.responseText);
        }
    }

    xhttp.open("POST", "/ai", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(`type=${formType}&input=${textInput}`);
})

// Move shooting star animation to position near cursor
function shootingStarOnCursor() {
    $("#shooting-star-container").css('left', mouseX);
    $("#shooting-star-container").css('top', mouseY);
    for (var i = 1; i <= 5; i++) {
        randLeft = randInt(-400, 400);
        randTop = randInt(-50, 50);
        $(`.shooting-star:nth-child(${i})`).css('left', randLeft);
        $(`.shooting-star:nth-child(${i})`).css('top', randTop);
    }

    $(".shooting-star").removeClass("shooting-star")
    repeatAnimation();
}

// Function to repeat animation once previous animation has finished (marked by the
// last shooting star)
function repeatAnimation() {
    var lastStar = document.getElementById("last-star");
    lastStar.addEventListener("animationend", function() {
        shootingStarOnCursor();
        setTimeout(function() {
            $(".night>div").addClass("shooting-star")
        }, 50);
    }, {once: true})

}

repeatAnimation();
