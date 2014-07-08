/**
  * @jsx React.DOM
  */

var LoginView = require('./login.jsx');

module.exports = React.createClass({

  getInitialState: function(){
    return {
      isUserConnected: false,
      isSearchPage: false
    }
  },


  render : function() {

    if(!this.state.isUserConnected){
      return (
        <LoginView>
        </LoginView>
      );
    }
    else{
      return (<div>Your are connected</div>)
    }

  }
});