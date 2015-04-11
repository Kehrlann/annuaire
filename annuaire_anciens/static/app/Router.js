//
// Globals
//

window.React = require('react');
window.Backbone = require('backbone');
window._ = require('underscore');
window.$ = require('jquery');
Backbone.$ = window.$;
//
// Dependencies
//

var RegisterView = require('./views/register.jsx'),
    NavbarView = require('./views/navbar.jsx'),
    SearchView = require('./views/search/search.jsx'),
    AncienView = require('./views/ancien/ancien.jsx');

var appGlobals = require('./AppGlobals.js');


var Router = Backbone.Router.extend({

    routes: {
        "search/:term": "search",
        "search": "search",
        "ancien/:id": "ancien",
        "me": "me",
        "*actions": "defaultRoute"
    },

    initialize: function() {

        // Finally, start up the history
        // WARNING: this should always be done at the END as it launches the routes, which may need the initialized objects
        Backbone.history.start({
            pushState: true
        });

        React.render(
          NavbarView({}),
          document.getElementById('js-navbar')
        );
    },

    defaultRoute: function(path) {
        $.ajax(
            {
                method: "GET",
                url: appGlobals.url.logged,
                success: function (data) {
                    var results = eval("(" + data + ")");
                    if(results.logged){
                        Backbone.history.navigate("/search", {trigger:true});
                    } else {
                        React.render(
                            RegisterView({}),
                            document.getElementById('js-main')
                        );
                    }
                }
            }
        );
    },


    /********************************************************************
     * Search dans l'annuaire                                           *
     *                                                                  *
     * @param term      (opt)   Recherche à effectuer immédiatement     *
     *                          lors du chargement de la page de        *
     *                          recherche.                              *
     ********************************************************************/
    search: function(term){
        React.render(
          SearchView({q: term}),
          document.getElementById('js-main')
        );
    },



    /********************************************************************
     * Affichage du profil d'un ancien.                                 *
     *                                                                  *
     * @param id      (obl)     Id de l'ancien à afficher (int)         *
     ********************************************************************/
    ancien: function(id){
        $.ajax
        (
            {
                method:"GET",
                url:appGlobals.url.ancien_complet(id),
                success:    function(data)
                            {
                                var ancien = eval("("+data+")");
                                React.render(
                                    AncienView({ancien: ancien, canEdit: true}),
                                    document.getElementById('js-main')
                                );
                            }
                ,
                error:      function(data)
                            {
                                Backbone.history.navigate("/search", { trigger : true });
                            }
            }
        );
    },


    /********************************************************************
     * Récupération de mes infos puis affichage de mon profil.          *
     ********************************************************************/
    me: function() {
        $.ajax
        (
            {
                method:"GET",
                url:appGlobals.url.whoami,
                success:    function(data)
                            {
                                // TODO
                                // TODO
                                // TODO
                                // TODO
                                // TODO
                                // TODO
                                // TODO
                                // TODO
                                // TODO
                                // TODO
                                // Créer mon compte ...
                                var ancien = eval("("+data+")");
                                Backbone.history.navigate("/ancien/"+ancien.id_ancien, {trigger:true});
                            }
                ,
                error:      function(data)
                            {
                                Backbone.history.navigate("/search");
                            }
            }
        );
    }

});


$(document).ready(function(){
    //
    // Patchs
    //
    // Patch Bootstrap popover to take a React component instead of a
    // plain HTML string (see http://jsfiddle.net/spicyj/q6hj7/)
    $.extend($.fn.popover.Constructor.DEFAULTS, {react: false});
    var oldSetContent = $.fn.popover.Constructor.prototype.setContent;
    $.fn.popover.Constructor.prototype.setContent = function() {
        if (!this.options.react) {
            return oldSetContent.call(this);
        }

        var $tip = this.tip();
        var title = this.getTitle();
        var content = this.getContent();

        $tip.removeClass('fade top bottom left right in');

        // If we've already rendered, there's no need to render again
        if (!$tip.find('.popover-content').html()) {
            // Render title, if any
            var $title = $tip.find('.popover-title');
            if (title) {
                React.renderComponent(title, $title[0]);
            } else {
                $title.hide();
            }

            React.renderComponent(
                content,
                $tip.find('.popover-content')[0]
            );
        }
    };

    new Router();
});





