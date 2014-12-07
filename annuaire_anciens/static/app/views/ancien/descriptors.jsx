/**
 * @jsx React.DOM
 */
var Simple = React.createClass({
        render:function(){
            if(this.props.value){
                var values = this.props.value.split("\n").map(
                    function(v){
                        return <span>{v}<br /></span> ;
                    }
                );

                var toRender = this.props.value;
                if(values.length > 1){
                    toRender = values;
                }

                return  <div className="row">
                    <div className="col-sm-2 custom-text-right-big-screen cutsom-descriptor">{this.props.label}</div>
                    <div className="col-sm-9">{toRender}</div>
                </div>;
            }
            else
                return <div></div>;
        }
    }
);

module.exports.Simple = Simple;

module.exports.LinkedIn = React.createClass({
        render:function(){
            return null;
        }
    }
);

module.exports.Adresse = React.createClass({
        formatVille:function(){
            var res = this.props.adresse.ville;
            if(this.props.adresse.code){
                res += " - ";
                res += this.props.adresse.code;
            }
            return res;
        },
        render:function(){
            var label = "Adresse";
            var descriptors = [];

            if (this.props.adresse.adresse){
                descriptors.push(<Simple label={label} value={this.props.adresse.adresse} />);
                label = "";
            }

            if (this.props.adresse.ville)
            {
                descriptors.push(<Simple label={label} value={this.formatVille()} />);
                label = "";
            }

            if (this.props.adresse.pays)
            {
                descriptors.push(<Simple label={label} value={this.props.adresse.pays} />);
            }

            return <div>{descriptors}</div>;
        }
    }
);
