/**
 * @jsx React.DOM
 */
var ExperienceForm  = require('./ancienExperienceForm.jsx');
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
        this.setState({currentView: views.exp});
    },

    /********************************************************
    *                                                       *
    *  Mettre à jour une expérience, puis la reloader       *
    *  depuis le serveur.                                   *
    *                                                       *
    *********************************************************/
    addExperience: function(id_experience, experience) {
        var ctrl = this;
        Q       (  $.ajax
                    (
                        {
                            method:     "POST",
                            url:        appGlobals.url.user.experience.add,
                            accept:     "application/json; charset=utf-8",
                            contentType:"application/json; charset=utf-8",
                            data:       JSON.stringify(experience),
                            processData:false
                        }
                    )
                )
        .then   (   function(data)
                    {
                        ctrl.setState({currentView: views.menu});
                        //experience.extend({ "debut" : experience.date_debut, "fin" : experience.date_fin});
                        ctrl.props.addExperience(experience);
                    }
                )
        .catch  (   function(err)
                    {
                        if(err && err.status == 400 && err.responseJSON && err.responseJSON.errors){
                            ctrl.setState({ errors : err.responseJSON.errors });
                        }
                    }
        );
    },
    render:function()
    {
        var inner;
        switch(this.state.currentView)
        {
            case views.exp:
                inner   =   <ExperienceForm     experience          =   {{}}
                                                handleCancel        =   {this.gotoMenu}
                                                handleUpdate        =   {this.addExperience}
                                                errors              =   {this.state.errors}
                            />;
                break;
            default:
                inner   =   <AdminMenu          addExperience       =   {this.gotoExperience}
                            />;
        }

        return  <div className="row custom-ancien-container-light experience-container" id="management">
                    {inner}
                </div>;
    }
});