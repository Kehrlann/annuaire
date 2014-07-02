//
// Globals
//

window.React = require('react');
window.Backbone = require('backbone');
window._ = require('underscore');
window.$ = require('jquery');
Backbone.$ = $;

//
// Dependencies
//

var RegisterView = require('./views/register.jsx');

var Router = Backbone.Router.extend({

    routes: {
        "*actions": "defaultRoute"
    },

    initialize: function() {

        // Finally, start up the history
        // WARNING: this should always be done at the END as it launches the routes, which may need the initialized objects
        Backbone.history.start({
            pushState: true
        });
    },

    defaultRoute: function(path) {
        // Default route

        console.log("defaultRoute, rendering RegisterView", document.getElementById('js-main'));
        // Render the register view
        React.renderComponent(
          RegisterView({}),
          document.getElementById('js-main')
        );

    }
});

$(function(){
    new Router();
});

