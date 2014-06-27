/**
  * @jsx React.DOM
  */


var PersonView = require('./PersonView.jsx');

module.exports = React.createClass({
  getInitialState: function(){
    return { isLoading: true };
  },

  componentWillMount: function(){
    // Listen to changes in the list and force re-rendering
    this.props.model.on('reset add change', function(){
      this.forceUpdate();
    }.bind(this));
  },

  componentDidMount: function(){
    // When the component is mounted, start fetching the data
    this.props.model.fetch().then((function(){
      // Changing the state will trigger render()
      this.setState({ isLoading: false });
    }).bind(this));
  },

  render : function() {
    // Before the model is fetched, display a loading indicator
    if(this.state.isLoading){
      return (<div className="container-fluid">Loading ...</div>);
    }

    // Once the model is fetched (isLoading is false) display the list of people

    // create an array of people
    var peopleList = [];
    // for each model inside the collection, create a subview and add it to the array
    if(this.props.model && this.props.model.models){
      _.forEach(this.props.model.models, function(person){
        peopleList.push(<PersonView model={person} />);
      }.bind(this));
    }

    // Return the complete template
    return (
      <div>
        <span>There are {peopleList.length} characters in the list </span>
        <ul>
          {peopleList}
        </ul>
      </div>
    );
  }
});