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


$(function() {
    $(".flex-item").click(function (event) {
        $(".flex-item").removeClass("show");
        $(this).addClass("show");
    })
})