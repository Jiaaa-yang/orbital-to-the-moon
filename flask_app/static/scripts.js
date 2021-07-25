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
