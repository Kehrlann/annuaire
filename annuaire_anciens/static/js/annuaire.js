function intermines_pagination_page(url){
    $.get(url, function(html) {
        $('#custom-pagination').replaceWith(html);
    });
    return false;
}

$(function(){
  $('#js-login-popover').popover({
      html : true,
      placement: "bottom",
      content: function() {
        return $("#js-login-form").html();
      }
  });
});

