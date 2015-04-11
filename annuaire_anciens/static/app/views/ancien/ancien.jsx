/**
 * @jsx React.DOM
 */
var AncienInfo  = require('./ancienInfo.jsx');
var AncienAdmin = require('./ancienAdmin.jsx');
var Experience  = require('./ancienExperience.jsx');
var appGlobals  = require('../../AppGlobals.js');
var Q           = require('q');

module.exports = React.createClass({
    getInitialState:function()
    {
        // Setup :  copier l'ancien dans le state, pour pouvoir
        //          le modifier librement
        return { ancien: this.props.ancien };
    },
    setPrimaire: function(id_experience){
        var ctrl = this;
        Q       (   $.ajax
                    (
                        {
                            method:     "PUT",
                            url:        appGlobals.url.user.experience.setPrimaire(id_experience)
                        }
                    )
                )
        .then   (   function(data)
                    {
                        ctrl.state.ancien.experiences.forEach   (   function(value)
                                                                    {
                                                                        value.actif = value.id_experience == id_experience;
                                                                    }
                                                                );
                        ctrl.setState({ancien: ctrl.state.ancien});
                    }
                )
        .catch  (   function(err)
                    {
                        // TODO : what do ???
                    }
                );
    },
    deleteExperience:function(){},
    render:function()
    {
        if(this.state.ancien == null)
        {
            return <div></div>;
        } else {

            var experiences = this.state.ancien.experiences.map(
                function(exp){
                    return  <Experience key                 =   {exp.id_experience}
                                        isPrimaire          =   {exp.actif}
                                        experience          =   {exp}
                                        canEdit             =   {this.props.canEdit}
                                        setPrimaire         =   {this.setPrimaire}
                                        deleteExperience    =   {this.deleteExperience}
                            />;
                }.bind(this)
            );

            return  <div className="container">
                        <div className="row">
                            <div className="col-lg-10 col-lg-offset-1">
                                <AncienAdmin    ancien={this.state.ancien} />
                                <AncienInfo     ancien={this.state.ancien} />
                                {experiences}
                            </div>
                        </div>
                    </div>;
        }
    }
});