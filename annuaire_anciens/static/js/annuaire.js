function intermines_pagination_page(url){
    $.get(url, function(html) {
        $('#custom-pagination').replaceWith(html);
    });
    return false;
}