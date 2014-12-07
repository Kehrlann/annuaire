/**
 * @jsx React.DOM
 */
var Ancien = require("./searchResult.jsx");
module.exports = React.createClass({
        render:function()   {
            var anciens = this.props.anciens.map(
                function (ancien)
                {
                    return  (
                        <Ancien ancien={ancien} />
                    );
                });

            var res = <div style={{marginTop : "10px"}} className="col-md-12 text-center">Pas de résultat !</div>;

            if(this.props.anciens && this.props.anciens.length > 0){
                res =   <div style={{marginTop : "10px"}} className="col-md-12">
                            {anciens}
                        </div>;
            }

            return  res;
        }
    }
);