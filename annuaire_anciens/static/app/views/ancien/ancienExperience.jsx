/**
 * @jsx React.DOM
 */
var Descriptor = require('./descriptors.jsx');
module.exports = React.createClass({
    render:function(){
        var experience = this.props.experience;
        var descriptors = [];

        // Infos basiques
        descriptors.push(<Descriptor.Simple label="Poste" value={experience.experience_poste} />);
        descriptors.push(<Descriptor.Simple label="Description" value={experience.experience_description} />);

        if(experience.adresse_adresse || experience.code || experience.ville || experience.pays){
            descriptors.push(<br />);
            descriptors.push(<Descriptor.Adresse adresse={experience} />);
        }

        //{{ br_not_empty(exp, ['adresse_adresse', 'adresse_code', 'ville_nom', 'pays_nom']) }}
        //{{ render_adresse(exp['adresse_adresse'], exp['ville_nom'], exp['adresse_code'], exp['pays_nom']) }}
        //
        //{{ br_not_empty(exp, ['experience_mail', 'experience_telephone', 'experience_mobile']) }}
        //{{ render_descriptor('Mail', exp['experience_mail']) }}
        //{{ render_descriptor('T&eacute;l&eacute;phone'|safe, exp['experience_telephone']) }}
        //{{ render_descriptor('Mobile', exp['experience_mobile']) }}



        return  <div className="row custom-ancien-container experience-container">
                    <div className="col-sm-10 col-sm-offset-1">
                        <div className="row">
                            <div className="custom-header-experience col-sm-10 col-sm-offset-2" >
                                {this.props.experience.entreprise}
                            </div>
                        </div>
                        {descriptors}
                    </div>
                </div>;
    }
});