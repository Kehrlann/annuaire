/**
 * @jsx React.DOM
 */
var ExperienceDescriptor = require('./ancienExperienceDescriptor.jsx');
var ExperienceForm = require('./ancienExperienceForm.jsx');
var appGlobals = require('../../helpers/AppGlobals.js');
var Q = require('q');

module.exports = React.createClass({
    getInitialState: function(){
        // Experience is the owner of the ancien.experience
        return { isEditing : false, experience : this.props.experience, errors : {} };
    },
    toggleEdit: function(){
        this.setState({ isEditing : !this.state.isEditing });
    },

    /********************************************************
     *                                                      *
     *  Récupérer une expérience depuis le serveur, afin de *
     *  mettre à jour l'affichage.                          *
     *                                                      *
     ********************************************************/
    loadExperienceFromServer: function(id_experience){
        return  Q   (   $.ajax
                        (
                            {
                                method:     "GET",
                                url:        appGlobals.url.user.experience.fetch(id_experience),
                                accept:     "application/json; charset=utf-8",
                                contentType:"application/json; charset=utf-8"
                            }
                        )
                    );
    },


    /********************************************************
     *                                                      *
     *  Mettre à jour une expérience, puis la reloader      *
     *  depuis le serveur.                                  *
     *                                                      *
     ********************************************************/
    updateExperience: function(id_experience, experience) {
        var ctrl = this;
        Q       (  $.ajax
                    (
                        {
                            method:     "PUT",
                            url:        appGlobals.url.user.experience.update(id_experience),
                            accept:     "application/json; charset=utf-8",
                            contentType:"application/json; charset=utf-8",
                            data:       JSON.stringify(experience),
                            processData:false
                        }
                    )
                )
        .then   (   function(data)
                    {
                        return ctrl.loadExperienceFromServer(id_experience);
                    }
                )
        .then   (   function(data)
                    {
                        var exp = eval("("+data+")");
                        ctrl.setState({ experience : exp, isEditing : false, errors : { } });
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


    /********************************************************
     *                                                      *
     *  Supprimer une expérience (duh)                      *
     *                                                      *
     ********************************************************/
    deleteExperience:function(id_experience)
    {
        this.props.deleteExperience(this.state.experience.id_experience);
    },

   /*********************************************************
    *                                                       *
    *  RENDER.                                              *
    *                                                       *
    *********************************************************/
    render:function(){
        var showElement;
        if (this.state.isEditing)
        {
            showElement =   <ExperienceForm         experience          =   {this.state.experience}
                                                    handleCancel        =   {this.toggleEdit}
                                                    handleUpdate        =   {this.updateExperience}
                                                    errors              =   {this.state.errors}
            />;
        }
        else
        {
            showElement =   <ExperienceDescriptor   experience          =   {this.state.experience}
                                                    handleEdit          =   {this.toggleEdit}
                                                    isPrimaire          =   {this.props.isPrimaire}
                                                    setPrimaire         =   {this.props.setPrimaire}
                                                    handleRemove        =   {this.deleteExperience}
                                                    canEdit             =   {this.props.canEdit}
                            />;
        }

        return  <div className="row custom-ancien-container experience-container">
                    {showElement}
                </div>;
    }
});