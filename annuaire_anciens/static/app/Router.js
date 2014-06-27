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

var HelloView = require('./views/HelloView.jsx'),
    PeopleListView = require('./views/people/PeopleListView.jsx'),
    People = require('./models/people');

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

        // Render the hello world view
        React.renderComponent(
          HelloView({}),
          document.getElementById('js-hello')
        );

        this.people = this.people || new People();

        // Render the people list
        React.renderComponent(
          PeopleListView({ model: this.people }),
          document.getElementById('js-people')
        );
    }
});

$(function(){
    new Router();
});

