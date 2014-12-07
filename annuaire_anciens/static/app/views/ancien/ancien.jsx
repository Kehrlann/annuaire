/**
 * @jsx React.DOM
 */
var AncienInfo = require('./ancienInfo.jsx');
var Experience = require('./ancienExperience.jsx');
module.exports = React.createClass({
    getInitialState:function()
    {
        return { ancien: null };
    },
    componentDidMount:function()
    {
        this.setState({ancien : this.props.ancien });
    },
    render:function()
    {
        if(this.state.ancien == null)
        {
            return <div></div>;
        } else {

            var experiences = this.state.ancien.experiences.map(
                function(exp){
                    return <Experience experience={exp} />;
                }
            );


            return  <div className="container">
                        <div className="row">
                            <div className="col-lg-10 col-lg-offset-1">
                                <AncienInfo ancien={this.state.ancien} />
                                {experiences}
                            </div>
                        </div>
                    </div>;
        }


    }
});