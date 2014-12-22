/**
 * @jsx React.DOM
 */
var ExperienceDescriptor = require('./ancienExperienceDescriptor.jsx');
var ExperienceForm = require('./ancienExperienceForm.jsx');

module.exports = React.createClass({
    getInitialState: function(){
        // Experience is the owner of the ancien.experience
        return { isEditing : false };
    },
    toggleEdit: function(){
        this.setState({ isEditing : !this.state.isEditing });
    },

    // Passer une expérience de "secondaire" à "primaire"
    handleSecondaire: function(){
    },
    render:function(){
        var showElement;
        if (this.state.isEditing)
        {
            showElement =   <ExperienceForm         experience          =   {this.props.experience}
                                                    handleCancel        =   {this.toggleEdit}
                                                    handleUpdate        =   {this.toggleEdit}
            />;
        }
        else
        {
            showElement =   <ExperienceDescriptor   experience          =   {this.props.experience}
                                                    handleEdit          =   {this.toggleEdit}
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