/**
 * @jsx React.DOM
 */
var ExperienceDescriptor = require('./ancienExperienceDescriptor.jsx');
var ExperienceForm = require('./ancienExperienceForm.jsx');

module.exports = React.createClass({
    getInitialState: function(){
        // Experience is the owner of the ancien.experience
        return { isEditing : false, experience : this.props.experience };
    },
    toggleEdit: function(){
        this.setState({ isEditing : !this.state.isEditing });
    },
    updateExperience: function(id_experience, experience) {
        $.ajax
        (
            {
                method:     "PUT",
                url:        appGlobals.url.user.experience.update(id_experience),
                accept:     "application/json; charset=utf-8",
                contentType:"application/json; charset=utf-8",
                data:       JSON.stringify(experience),
                processData:false,
                success:    function(data)  {   console.log("~~~~~~~~~~~~~~~~~> SUCCESS update experience");
                                                console.log(data);
                                            },
                error:      function(data)  {   console.log("~~~~~~~~~~~~~~~~~> FAIL update experience");
                                                console.log(data);
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
            />;
        }
        else
        {
            showElement =   <ExperienceDescriptor   experience          =   {this.state.experience}
                                                    handleEdit          =   {this.toggleEdit}
                                                    isPrimaire          =   {this.props.isPrimaire}
                                                    setPrimaire         =   {this.props.setPrimaire}
                                                    handleRemove        =   {this.toggleEdit}
                                                    canEdit             =   {this.props.canEdit}
                            />;
        }

        return  <div className="row custom-ancien-container experience-container">
                    {showElement}
                </div>;
    }
});