var cookie = require('jquery.cookie');

module.exports.setIdAncien =
    function(id){
        cookie('id_ancien', id);
    };

module.exports.getIdAncien =
    function()
    {
        return cookie('id_ancien');
    };

module.exports.isThisMe =
    function(idAncien)
    {
        return idAncien == cookie('id_ancien');
    };