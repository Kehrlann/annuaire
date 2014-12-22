/**
 * @jsx React.DOM
 */
var Descriptor = require('./descriptors.jsx');
module.exports = React.createClass({
    handleEditClick : function(e) {
        e.preventDefault();
        this.props.handleEdit();
    },
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

        var entreprise = this.props.experience.site ?   <a href={this.props.experience.site} target="_blank">{this.props.experience.entreprise}</a>
                                                    :   this.props.experience.entreprise;

        var boutonPrimaireSecondaire;
        if (this.props.experience.actif) {
            boutonPrimaireSecondaire =  <a className="btn btn-warning btn-xs experience-principale">
                                            <i className="glyphicon glyphicon-star"></i> <span>Principale</span>
                                        </a>;
        } else {
            boutonPrimaireSecondaire =  <a className="btn btn-default btn-xs" onClick={this.props.setPrimaire.bind(this, this.props.experience.id_experience)}>
                                            <i className="glyphicon glyphicon-star-empty"></i> <span>Secondaire</span>
                                        </a>;
        }


        return  <div className="col-sm-12">
                    <div className="row">
                        <div className="custom-header-experience col-sm-10 col-sm-offset-2" >
                        {entreprise}
                        </div>
                    </div>
                    {descriptors}
                    <div className="row" style={{marginTop:"20px"}}>
                        <div style={{display:"inline"}} className="col-sm-10 col-sm-offset-2">
                            <a className="btn btn-xs btn-success" type="button" onClick={this.handleEditClick}>
                                <i className="glyphicon glyphicon-edit"></i> Modifier
                            </a>
                            &nbsp;
                            {boutonPrimaireSecondaire}
                            &nbsp;
                            <a className="btn btn-xs btn-danger" type="button" onClick={this.props.handleRemove}>
                                <i className="glyphicon glyphicon-remove"></i> Effacer
                            </a>
                        </div>
                    </div>
                </div>;
    }
});