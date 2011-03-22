function on_load() {
    for (var i = 0, len = on_load.load.length; i < len; i++) {
        on_load.load[i]();
    }
    return true;
}

on_load.load = []
on_load.add = function(f) {
    on_load.load.push(f);
};

function OfficeDesc(obj, key) {
    // Reset all the buttons
    $(".office").css("color","#336699");
    // Highlight the current office
    $(obj).css("color", "red");
    // Fetch the data.
    $.ajax({
        url: "/json/office/" + key + "/",
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
