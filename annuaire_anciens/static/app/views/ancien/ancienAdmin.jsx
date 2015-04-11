/**
 * @jsx React.DOM
 */
var ExperienceForm  = require('./ancienExperience.jsx');
var AdminMenu       = require('./ancienAdminMenu.jsx');
var appGlobals      = require('../../AppGlobals.js');
var Q               = require('q');

var views = {   menu :  "menu",
                exp  :  "exp",
                pass :  "pass"
            };

module.exports = React.createClass({
    getInitialState:function(){
        return { currentView: views.menu, errors: {} };
    },
    gotoMenu:function(){
        this.setState({currentView: views.menu});
    },
    gotoExperience:function(){
        console.log("GOTO EXP");
        this.setState({currentView: views.exp});
    },
    render:function()
    {
        console.log(this.state.currentView);
        switch(this.state.currentView)
        {
            case views.menu:
                return <AdminMenu />;
            case views.exp:
                return  <ExperienceForm     experience          =   {{}}
                                            handleCancel        =   {this.gotoMenu}
                                            handleUpdate        =   {this.gotoMenu}
                                            errors              =   {this.state.errors}
                        />;
            default:
                return  <AdminMenu          addExperience       =   {this.gotoExperience}
                        />;
        }
    }
});