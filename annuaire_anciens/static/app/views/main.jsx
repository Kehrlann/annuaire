/**
  * @jsx React.DOM
  */

module.exports = React.createClass({

  getInitialState: function(){
    return {}
  },
  render : function() {
    return <div>Main {this.props.term}</div>;
  }
});