/**
 * @jsx React.DOM
 */
var Descriptor = require('./descriptors.jsx');
module.exports = React.createClass({
    render:function(){
        var experience = this.props.experience;
        var descriptors = [];

        // Infos basiques
        descriptors.push(<Descriptor.Simple label="Poste" value={experience.poste} />);
        descriptors.push(<Descriptor.Simple label="Description" value={experience.description} />);

        if(experience.adresse || experience.code || experience.ville || experience.pays){
            descriptors.push(<br />);
            descriptors.push(<Descriptor.Adresse adresse={experience} />);
        }

        if(experience.mail || experience.telephone || experience.mobile){
            descriptors.push(<br />);
            descriptors.push(<Descriptor.Simple label="Mail" value={experience.mail} mail={true} />);
            descriptors.push(<Descriptor.Simple label="Téléphone" value={experience.telephone} />);
            descriptors.push(<Descriptor.Simple label="Mobile" value={experience.mobile} />);
        }

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