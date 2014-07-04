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

var RegisterView = require('./views/register.jsx'),
    NavbarView = require('./views/navbar.jsx');

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

        React.renderComponent(
          NavbarView({}),
          document.getElementById('js-navbar')
        );
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





