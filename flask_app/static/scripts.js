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