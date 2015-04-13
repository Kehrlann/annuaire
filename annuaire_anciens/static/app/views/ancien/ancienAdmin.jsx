/**
 * @jsx React.DOM
 */
var ExperienceForm  = require('./ancienExperienceForm.jsx');
var AdminMenu       = require('./ancienAdminMenu.jsx');
var appGlobals      = require('../../helpers/AppGlobals.js');
var Q               = require('q');
var pays            = require('../../data/pays.js');

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
                        var exp = eval("("+data+")");
                        if(exp && exp.id_experience)
                        {
                            var selected_pays = experience.pays ? pays.filter(function(p){ return p.value == experience.pays; })[0].name : null;
                            ctrl.setState({currentView: views.menu});
                            var new_exp = $.extend({}, experience, { debut : experience.date_debut, fin : experience.date_fin, id_experience : exp.id_experience, pays : selected_pays });
                            console.log(new_exp);
                            ctrl.props.addExperience(new_exp);
                        }

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
                                                visible             =   {this.props.ancien.actif}
                                                toggleVisible       =   {this.props.toggleVisible}
                            />;
        }

        return  <div className="row custom-ancien-container-light experience-container" id="management">
                    {inner}
                </div>;
    }
});