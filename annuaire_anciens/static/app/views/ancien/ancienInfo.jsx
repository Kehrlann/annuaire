/**
 * @jsx React.DOM
 */
var Descriptor = require('./descriptors.jsx');
module.exports = React.createClass({
    getNom: function(){
        var res = "";
        if(this.props.ancien.prenom){
            res = this.props.ancien.prenom + " ";
        }
        res += this.props.ancien.nom;
        return res;
    },
    getEcole: function(){
        var res = "";
        if(this.props.ancien.ecole){
            res = this.props.ancien.ecole + " ";
        }
        res += this.props.ancien.promo;
        return res;
    },
    render:function(){
        var ancien = this.props.ancien;
        var descriptors = [];

        // Infos basiques
        descriptors.push(<Descriptor.Simple label="Nom" value={this.getNom()} />);
        descriptors.push(<Descriptor.Simple label="Promo" value={this.getEcole()} />);
        descriptors.push(<Descriptor.Simple label="Diplôme" value={ancien.diplome} />);


        // Infos de contact (mails, site, linkedin)
        if(ancien.mail_perso || ancien.mail_asso || ancien.site || ancien.url_linkedin)
            descriptors.push(<br />);

        descriptors.push(<Descriptor.Simple label="Mail perso" value={ancien.mail_perso} mail={true} />);
        descriptors.push(<Descriptor.Simple label="Mail à vie" value={ancien.mail_asso} mail={true} />);
        /*{{ render_linkedin(ancien) }}*/
        // TODO
        // TODO
        // TODO
        // TODO
        // TODO
        // TODO
        // TODO
        // TODO
        // TODO
        descriptors.push(<Descriptor.Simple label="Site" value={ancien.site} link={true} />);

        // Adresses perso
        if(ancien.adresse){
            descriptors.push(<br />);
            descriptors.push(<Descriptor.Adresse adresse={ancien.adresse} />);
        }

        // Telephone
        if(ancien.telephone || ancien.mobile)
        {
            descriptors.push(<br />);
            descriptors.push(<Descriptor.Simple label="Téléphone" value={ancien.telephone} />);
            descriptors.push(<Descriptor.Simple label="Mobile" value={ancien.mobile}  />);
        }

        if(ancien.delegue){
            descriptors.push(<br />);
            descriptors.push(<Descriptor.Simple label="" value="Délégué de promotion"  />);
        }

        return  <div className="row custom-ancien-container" id="info-perso">
                    <div className="col-sm-4 custom-text-center-big-screen" style={{marginBottom:"15px;"}} id="photo-perso">
                        <img src={appGlobals.url.photo(this.props.ancien.photo)} className="custom-img span4"/>
                    </div>
                    <div className="col-sm-8 text-left" id="info-perso-text">
                        {descriptors}
                    </div>
                </div>;
    }
});