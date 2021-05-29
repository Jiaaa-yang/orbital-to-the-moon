$(function() {
    $(".flex-item").click(function (event) {
        $(".flex-item").removeClass("show");
        $(this).addClass("show");
    })
})