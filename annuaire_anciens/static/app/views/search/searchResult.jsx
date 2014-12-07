/**
 * @jsx React.DOM
 */
module.exports = React.createClass({
        buildUrl: function(){
            return "/ancien/"+this.props.ancien.id;
        },
        nom: function() {
            var result = "";
            var prenom = this.props.ancien.prenom;
            if (prenom != null && prenom != ""){
                result += prenom;
                result += " ";
            }
            var nom = this.props.ancien.nom;
            if(nom != null && nom != ""){
                result += nom;
            }
            return result;
        },
        entreprise: function() {
            var entreprise = this.props.ancien.entreprise;
            if(entreprise)
                return entreprise;
            else
                return "";
        },
        adresse: function() {
            var result = "";
            var ville = this.props.ancien.ville;
            var pays = this.props.ancien.pays;
            if (ville!=null && ville != ""){
                result += ville;
                result += " ";
            }
            if(pays != null && pays != ""){
                result += "(";
                result += pays;
                result += ")";
            }
            return result;
        },
        render:function(){
            return  <a href={this.buildUrl()} target="_blank">
                        <div className="row annuaire-row">
                            <div className="col-sm-3">{this.nom()}</div>
                            <div className="col-sm-4">{this.entreprise()}</div>
                            <div className="col-sm-3">{this.adresse()}</div>
                            <div className="col-sm-2 custom-text-right-big-screen">{this.props.ancien.ecole} {this.props.ancien.promo}</div>
                        </div>
                    </a>;
        }
    }
);