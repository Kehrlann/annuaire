/**
 * @jsx React.DOM
 */

module.exports.serializeToJson =
    function(domNode) {
        var res = {};
        $(domNode).find("input").each(
            function(index, input){
                res[$(input).attr("name")] = $(input).val();
            }
        );
        return res;
    };