var $ = require('jquery');

module.exports = function(queryString){
    var params = {};
    if(queryString){
        $.each(
            $.map(decodeURI(queryString).split(/&/g),function(el,i){
                var aux = el.split('='), o = {};
                if(aux.length >= 1){
                    var val = undefined;
                    if(aux.length == 2)
                        val = aux[1];
                    o[aux[0]] = val;
                }
                return o;
            }),
            function(i, o){
                $.extend(params,o);
            }
        );
    }
    return params;
};