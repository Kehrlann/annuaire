var $ = require('jquery');
require('jquery.cookie');

module.exports.setIdAncien =
    function(id){
        $.cookie('id_ancien', id);
    };

module.exports.getIdAncien =
    function()
    {
        return $.cookie('id_ancien');
    };

module.exports.isThisMe =
    function(idAncien)
    {
        return idAncien == $.cookie('id_ancien');
    };

module.exports.removeIdAncien =
    function()
    {
        $.removeCookie('id_ancien');
    };

module.exports.isLogged =
    function()
    {
        return $.cookie('id_ancien') != null;
    };