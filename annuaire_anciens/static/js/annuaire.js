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
        return $("#js-login-form-content").html();
      }
  });

  $('.navbar').on('submit', '#js-login-form', function(e){
    // prevent the form from posting
    e.preventDefault();

    var form = $(e.target);
    var loginUrl = form.attr('action');

    var $this = $(e.target);

    $.ajax({
      type: "POST",
      url: loginUrl,
      data: form.serialize(),
      success: function(data){
        console.log("Success : "+data);
        window.location.replace(data);
      },
      error: function(){
        var message = "<div class='alert alert-danger'><button type='button' class='close' data-dismiss='alert'>&times;</button>Erreur de login !</div>";
        $this.find('.error').html(message);
      }
    });


  });
});

