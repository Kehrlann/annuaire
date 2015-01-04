/**
 * @jsx React.DOM
 */
var Form = require('./forms.jsx');
var formHelper = require('../helpers/formHelper');
module.exports = React.createClass({
    handleUpdate : function(e){
        e.preventDefault();
        var exp = formHelper.serializeToJson(this.refs.experienceForm.getDOMNode());
        this.props.handleUpdate(this.props.experience.id_experience, exp);
    },
    render:function(){
        var experience = this.props.experience;
        var descriptors = [];

        // Infos basiques
        descriptors.push(<Form.Simple   label="Entreprise"      value={experience.entreprise}   name="entreprise"   />);
        descriptors.push(<Form.Simple   label="Poste"           value={experience.poste}        name="poste"        />);
        descriptors.push(<Form.TextArea label="Description"     value={experience.description}  name="description"  />);
        descriptors.push(<Form.Date     label="Date début"      value={experience.debut}        name="date_debut"   />);
        descriptors.push(<Form.Date     label="Date fin"        value={experience.fin}          name="date_fin"     />);
        descriptors.push(<br />);
        descriptors.push(<Form.Simple   label="Adresse"         value={experience.adresse}      name="adresse"      />);
        descriptors.push(<Form.Simple   label="Ville"           value={experience.ville}        name="ville"        />);
        descriptors.push(<Form.Simple   label="C. Postal"       value={experience.code}         name="code"         />);
        descriptors.push(<Form.Simple   label="Pays"            value={experience.pays}         name="pays"         />);
        descriptors.push(<br />);
        descriptors.push(<Form.Simple   label="Mail"            value={experience.mail}         name="mail"         />);
        descriptors.push(<Form.Simple   label="Site"            value={experience.site}         name="site"         />);
        descriptors.push(<Form.Simple   label="Téléphone"       value={experience.telephone}    name="telephone"    />);
        descriptors.push(<Form.Simple   label="Mobile"          value={experience.mobile}       name="mobile"       />);

        return  <div>
                    <form ref="experienceForm">
                        {descriptors}
                    </form>
                    <div className="row"  style={{marginTop:"20px"}}>
                        <div className="col-sm-9 col-sm-offset-2"  >
                            <a className="btn btn-success btn-sm" onClick={this.handleUpdate}>Mettre &agrave; jour</a>
                            <a className="btn btn-warning btn-sm pull-right" onClick={this.props.handleCancel}>Annuler</a>
                        </div>
                    </div>
                </div>;
    }
});