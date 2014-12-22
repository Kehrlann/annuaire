/**
 * @jsx React.DOM
 */
var Form = require('./forms.jsx');
module.exports = React.createClass({
    handleUpdate : function(e){
        e.preventDefault();
        this.props.handleUpdate();
    },
    handleCancel : function(e){
        e.preventDefault();
        this.props.handleCancel();
    },
    render:function(){
        var experience = this.props.experience;
        var descriptors = [];

        // Infos basiques
        descriptors.push(<Form.Simple   label="Entreprise"      value={experience.entreprise}   name="entreprise"    />);
        descriptors.push(<Form.Simple   label="Poste"           value={experience.poste}        name="poste"         />);
        descriptors.push(<Form.TextArea label="Description"     value={experience.description}  name="description"   />);
        //descriptors.push(<Form.Date     label="Date début"      value={experience.date_debut}   name="date_debut"    />);
        //descriptors.push(<Form.Date     label="Date fin"        value={experience.date_fin}     name="date_fin"      />);
        descriptors.push(<br />);
        descriptors.push(<Form.Simple   label="Adresse"         value={experience.adresse}      name="adresse"       />);
        descriptors.push(<Form.Simple   label="Ville"           value={experience.ville}        name="ville"         />);
        descriptors.push(<Form.Simple   label="C. Postal"       value={experience.code}         name="code"          />);
        descriptors.push(<Form.Simple   label="Pays"            value={experience.pays}         name="pays"          />);
        descriptors.push(<br />);
        descriptors.push(<Form.Simple   label="Mail"            value={experience.mail}         name="mail"          />);
        descriptors.push(<Form.Simple   label="Site"            value={experience.site}         name="site"          />);
        descriptors.push(<Form.Simple   label="Téléphone"       value={experience.telephone}    name="telephone"     />);
        descriptors.push(<Form.Simple   label="Mobile"          value={experience.mobile}       name="mobile"        />);

        return  <div>
                    {descriptors}
                    <div className="control-group col-sm-offset-2">
                        <div className="controls" style={{marginTop:"20px"}}>
                            <a className="btn btn-success btn-sm" onClick={this.handleUpdate}>Mettre &agrave; jour</a>
                            <a className="btn btn-warning btn-sm pull-right" onClick={this.handleCancel}>Annuler</a>
                        </div>
                    </div>
                </div>;
    }
});