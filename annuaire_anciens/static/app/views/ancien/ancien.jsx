/**
 * @jsx React.DOM
 */
var AncienInfo  = require('./ancienInfo.jsx');
var AncienAdmin = require('./ancienAdmin.jsx');
var Experience  = require('./ancienExperience.jsx');
var appGlobals  = require('../../helpers/AppGlobals.js');
var Q           = require('q');

module.exports = React.createClass({

    /********************************************************
     *                                                      *
     *  Setup : copier l'ancien dans le state, pour pouvoir *
     *  le modifier librement. C'est ce controller qui a    *
     *  la main sur l'ancien :o)                            *
     *                                                      *
     ********************************************************/
    getInitialState:function()
    {
        return { ancien: this.props.ancien };
    },

    /********************************************************
     *                                                      *
     *  Comme l'ancien est passé dans le state depuis les   *
     *  props, il faut écouter le changement de props pour  *
     *  mettre le state à jour.                             *
     *                                                      *
     *  Sinon, quand on navigate via Backbone de l'ancien 1 *
     *  à l'ancien 2, pas de refresh ...                    *
     *                                                      *
     ********************************************************/
    componentWillReceiveProps:function(nextProps)
    {
        if(nextProps && nextProps.ancien)
        {
            this.setState({ ancien : nextProps.ancien });
        }
    },

    /********************************************************
     *                                                      *
     *  Ajouter une expérience à la liste des expériences   *
     *  de l'ancien. Penser à les classer par "actif", puis *
     *  par ordre croissant de date_début.                  *
     *                                                      *
     ********************************************************/
    addExperience:function(experience)
    {
        console.log(experience);
        console.log(this.state.ancien.experiences);
        this.state.ancien.experiences.push(experience);

        var sortExperiences =
            function(exp1, exp2)
            {
                if(exp1.actif && exp2.actif)
                {
                    return 0;
                }
                else if (exp1.actif)
                {
                    return -1;
                }
                else if (exp2.actif)
                {
                    return 1;
                }
                else if(exp1.date_debut && exp2.date_debut)
                {
                    return exp1.date_debut > exp2.date_debut ? -1 : 1;
                }
                else if(exp1.date_debut)
                {
                    return -1;
                }
                else if(exp2.date_debut)
                {
                    return 1;
                }
                else
                {
                    return 0;
                }
            };

        this.state.ancien.experiences = this.state.ancien.experiences.sort(sortExperiences);
        this.setState({ancien : this.state.ancien});
    },

    /********************************************************
     *                                                      *
     *  Supprimer une expérience (duh)                      *
     *                                                      *
     ********************************************************/
    deleteExperience:function(id_experience)
    {
        var ctrl = this;
        Q       (   $.ajax
                    (
                        {
                            method:     "DELETE",
                            url:        appGlobals.url.user.experience.remove(id_experience)
                        }
                    )
                )
        .then   (   function(data)
                    {
                        ctrl.state.ancien.experiences = ctrl.state.ancien.experiences.filter(
                                                            function(value)
                                                            {
                                                                return value.id_experience != id_experience;
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

    /********************************************************
     *                                                      *
     *  Passer une certaine expérience à "primaire", en     *
     *  passant toutes les autres à "secondaire", puis      *
     *  re-render.                                          *
     *                                                      *
     ********************************************************/
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

    /********************************************************
     *                                                      *
     *  Passer ma fiche à visible ou invisble dans          *
     *  l'annuaire.                                         *
     *                                                      *
     ********************************************************/
    toggleVisible: function(){
        var ctrl = this;
        console.log("TOGGLE VISIBLE");
        Q       (   $.ajax
                    (
                        {
                            method:     "PUT",
                            url:        appGlobals.url.user.toggleVisible
                        }
                    )
                )
        .then   (   function(data)
                    {
                        var resp = eval("("+data+")");
                        console.log(resp);

                        if(resp && resp.hasOwnProperty("actif"))
                        {
                            ctrl.state.ancien.actif = resp.actif;
                            ctrl.setState({ancien: ctrl.state.ancien});
                        }
                    }
                )
        .catch  (   function(err)
                    {
                        // TODO : what do ???
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
                    return  <Experience key                 =   {exp.id_experience}
                                        isPrimaire          =   {exp.actif}
                                        experience          =   {exp}
                                        canEdit             =   {this.props.canEdit}
                                        setPrimaire         =   {this.setPrimaire}
                                        deleteExperience    =   {this.deleteExperience}
                            />;
                }.bind(this)
            );

            return  <div className="container" id="ancien-container">
                        <div className="row">
                            <div className="col-lg-10 col-lg-offset-1">
                                <AncienAdmin    ancien          =   {this.state.ancien}
                                                addExperience   =   {this.addExperience}
                                                visible         =   {this.state.ancien.actif}
                                                toggleVisible   =   {this.toggleVisible}
                                />
                                <AncienInfo     ancien={this.state.ancien} />
                                {experiences}
                            </div>
                        </div>
                    </div>;
        }
    }
});