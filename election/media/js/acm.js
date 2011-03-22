function office_dialog(obj, url) {
    // Reset all the buttons
    $(".office").css("color", "#336699");
    // Highlight the current office
    $(obj).css("color", "red");
    // Fetch the data.
    $.ajax({
        url: url,
        success: function(office) {
            $("#office_info").find("#title").text(office.title);
            $("#office_info").find("#desc_in").html(office.description);
            $("#office_info").show();
        }
    });
    $("#office_info").find("#close").bind("click", function() {
        $("#office_info").hide();
        // Undo obj stuff
        $(".office").css("color","#336699");
        return false;
    });
}
