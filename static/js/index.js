$(document).ready(function () {
    $("#navbar ul li").mouseenter(function () {
        $(this).addClass("active");
    });
    $("#navbar ul li").mouseleave(function () {
        $(this).removeClass("active");
    });
});
$(document).ready(function() {
    $("#AboutUs").click(function () {
        $("#div-AboutUs").fadeToggle();
    });
});