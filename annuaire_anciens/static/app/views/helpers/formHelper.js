module.exports.serializeToJson =
    function(domNode) {
        var res = {};
        $(domNode).find("input, textarea, select").each(
            function(index, input){
                res[$(input).attr("name")] = $(input).val();
            }
        );
        return res;
    };