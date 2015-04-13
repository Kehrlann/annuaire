//
// Globals
//

window.React        = require('react');
window.Backbone     = require('backbone');
window._            = require('underscore');
window.$            = require('jquery');
Backbone.$          = window.$;
//
// Dependencies
//

var RegisterView    = require('./views/register.jsx'),
    NavbarView      = require('./views/navbar.jsx'),
    SearchView      = require('./views/search/search.jsx'),
    AncienView      = require('./views/ancien/ancien.jsx');

var appGlobals      = require('./helpers/AppGlobals.js');
var cookie          = require('./helpers/cookies.js');
var Q               = require('q');
var queryString     = require('./helpers/queryString');


var _requireLogin   =   function ()
                        {
                            if(!cookie.isLogged())
                            {
                                Backbone.history.navigate("/register", {trigger:true});
                                return false;
                            }

                            return true;
                        };

var _getCookie      =   function()
                        {
                            var deferred = Q.defer();

                            // Get session cookie
                            Q       (   $.ajax
                                        (
                                            {
                                                method: "GET",
                                                url:    appGlobals.url.whoami
                                            }
                                        )
                                    )
                            .then   (   function(data)
                                        {
                                            var ancien = eval("("+data+")");

                                            if(ancien && ancien.id_ancien)
                                            {
                                                cookie.setIdAncien(ancien.id_ancien);
                                            }
                                            else
                                            {
                                                cookie.removeIdAncien();
                                            }
                                            deferred.resolve();
                                        }
                                    )
                            .catch  (   function(error)
                                        {
                                            if(error.status == 401)
                                            {
                                                cookie.removeIdAncien();
                                                Backbone.history.navigate("/register", {trigger:true});
                                                deferred.resolve();
                                            }
                                            else
                                            {
                                                // TODO : what do ???
                                                deferred.reject(error);
                                            }
                                        }
                                    );

                            return deferred.promise;
                        };

var Router = Backbone.Router.extend({

    routes: {
        "search/*qs":       "search",
        "search":           "search",
        "ancien/:id":       "ancien",
        "register":         "register",
        "login":            "login",
        "logout":           "logout",
        "*actions":         "defaultRoute"
    },

    initialize: function() {

        Q.when  (_getCookie())
        .then   (   function()
                    {
                        // Finally, start up the history
                        // WARNING: this should always be done at the END as it launches the routes, which may need the initialized objects
                        Backbone.history.start({
                            pushState: true
                        });

                        React.render(
                          <NavbarView />,
                          document.getElementById('js-navbar')
                        );
                    }
                );

    },

    defaultRoute: function(path) {
        Backbone.history.navigate("/search", {trigger:true});
    },


    /********************************************************************
     *                                                                  *
     * Register                                                         *
     *                                                                  *
     ********************************************************************/
    register: function(){
        React.render    (   <RegisterView />,
                            document.getElementById('js-main')
                        );
    },

    /********************************************************************
     *                                                                  *
     * Log-in                                                           *
     *                                                                  *
     ********************************************************************/
    login: function(){
        Q.when  (_getCookie())
        .then   (   function()
                    {
                        Backbone.history.navigate("/search", {trigger:true});
                    }
                );
    },

    /********************************************************************
     *                                                                  *
     * Log-in                                                           *
     *                                                                  *
     ********************************************************************/
    logout: function(){
        cookie.removeIdAncien();
        Backbone.history.navigate("/register", {trigger:true});
    },

    /********************************************************************
     * Search dans l'annuaire                                           *
     *                                                                  *
     * @param qs     (opt)      Recherche à effectuer immédiatement     *
     *                          lors du chargement de la page de        *
     *                          recherche, sous forme de queryString.   *
     *                                                                  *
     ********************************************************************/
    search: function(qs){
        if(_requireLogin())
        {
            var query = queryString(qs);
            console.log(query);
            console.log(qs);
            React.render(
              <SearchView query={query.q} page={query.p} />,
              document.getElementById('js-main')
            );
        }
    },



    /********************************************************************
     * Affichage du profil d'un ancien.                                 *
     *                                                                  *
     * @param id      (obl)     Id de l'ancien à afficher (int)         *
     ********************************************************************/
    ancien: function(id){
        if(_requireLogin())
        {
            $.ajax
            (
                {
                    method:"GET",
                    url:appGlobals.url.ancien_complet(id),
                    success:    function(data)
                                {
                                    var ancien = eval("("+data+")");
                                    React.render(
                                        <AncienView ancien={ancien} canEdit={true} />,
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
        }

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
                React.render(title, $title[0]);
            } else {
                $title.hide();
            }

            React.render(
                content,
                $tip.find('.popover-content')[0]
            );
        }
    };

    new Router();
});





