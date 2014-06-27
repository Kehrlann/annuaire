/**
  * @jsx React.DOM
  */

module.exports = React.createClass({
  componentWillMount: function(){
    // Listen to changes in the name and force re-rendering
    this.props.model.on('change:name', function(){
      this.forceUpdate();
    }.bind(this));
  },

  render : function() {
    // Return the complete template
    return (
      <li>{this.props.model.get('name')}</li>
    );
  }
});