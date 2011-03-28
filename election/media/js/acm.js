function office_dialog(office_url) {
  $.ajax({
    url: office_url,
    success: function (office) {
      var x = $("<div>" + office.description + "</div>");
      x.dialog({
        title: office.title,
      });
    }
  });
}
