/**
 * @jsx React.DOM
 */
var AncienInfo = require('./ancienInfo.jsx');
var Experience = require('./ancienExperience.jsx');
module.exports = React.createClass({
    getInitialState:function()
    {
        // Setup :  copier l'ancien dans le state, pour pouvoir
        //          le modifier librement
        return { ancien: this.props.ancien };
    },
    setPrimaire: function(id_experience){
        $.ajax
        (
            {
                method:     "PUT",
                url:        appGlobals.url.user.experience.setPrimaire(id_experience),
                success:    function(data)  {   this.state.ancien.experiences.forEach
                                                (
                                                    function(value) {
                                                        value.actif = value.id_experience == id_experience;
                                                    }
                                                );
                                                this.setState({ancien: this.state.ancien});
                                            }   .bind(this),
                error:      function(data)  {
                                            }
            }
        );
    },
    render:function()
    {
        if(this.state.ancien == null)
        {
            return <div></div>;
        } else {

            var experiences = this.state.ancien.experiences.map(
                function(exp){
                    return  <Experience key             =   {exp.id_experience}
                                        isPrimaire      =   {exp.actif}
                                        experience      =   {exp}
                                        canEdit         =   {this.props.canEdit}
                                        setPrimaire     =   {this.setPrimaire}
                            />;
                }.bind(this)
            );

            return  <div className="container">
                        <div className="row">
                            <div className="col-lg-10 col-lg-offset-1">
                                <AncienInfo ancien={this.state.ancien} />
                                {experiences}
                            </div>
                        </div>
                    </div>;
        }
    }
});