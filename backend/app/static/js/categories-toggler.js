$( document ).ready(function() {
    buttons = $(".cat-btn");

    buttons.on("click", function() {
        target = $(this).attr("data");

        parent_cat = $(this).parents(".category").attr("class").split(/\s+/)[0];
        $("." + parent_cat + " .subcat-items").each(function() {
            $(this).css("display", "none");
        });

        $("." + parent_cat + " .cat-btn").each(function() {
            $(this).removeClass("cat-btn-active");
        });

        $(this).addClass("cat-btn-active");

        $("." + target).css("display", "flex");

    });
});