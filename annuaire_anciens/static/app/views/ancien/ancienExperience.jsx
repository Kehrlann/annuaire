/**
 * @jsx React.DOM
 */
var ExperienceDescriptor = require('./ancienExperienceDescriptor.jsx');
var ExperienceForm = require('./ancienExperienceForm.jsx');
var appGlobals = require('../../AppGlobals.js');
var Q = require('q');

module.exports = React.createClass({
    getInitialState: function(){
        // Experience is the owner of the ancien.experience
        return { isEditing : false, experience : this.props.experience, errors : {} };
    },
    toggleEdit: function(){
        this.setState({ isEditing : !this.state.isEditing });
    },
    refreshExperience: function(id_experience){
        return  Q   (   $.ajax
                        (
                            {
                                method:     "GET",
                                url:        appGlobals.url.user.experience.update(id_experience),
                                accept:     "application/json; charset=utf-8",
                                contentType:"application/json; charset=utf-8"
                            }
                        )
                    );
    },
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
                        return ctrl.refreshExperience(id_experience);
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
                                                    handleRemove        =   {this.props.deleteExperience}
                                                    canEdit             =   {this.props.canEdit}
                            />;
        }

        return  <div className="row custom-ancien-container experience-container">
                    {showElement}
                </div>;
    }
});