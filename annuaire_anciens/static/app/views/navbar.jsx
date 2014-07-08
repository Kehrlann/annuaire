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
        <LoginView></LoginView>
      );
    }
    else{
      return (
        <div>
          <div className="nav navbar-nav navbar-right">
              <a className='btn btn-default navbar-btn hidden-xs' href="#">Mon compte</a>
              <a className='btn btn-link navbar-btn hidden-xs' href="#">D&eacute;connexion</a>
              <a className='btn btn-default navbar-btn visible-xs' href="#"><span className="glyphicon glyphicon-user"></span></a>
              <a className='btn btn-danger navbar-btn visible-xs' href="#"><span className="glyphicon glyphicon-log-out"></span></a>
          </div>
          <form className="navbar-form navbar-left nav-search-zone" role="search">
            <span className="glyphicon glyphicon-search"></span>
            <input type="text" autocomplete="off" ref="fulltext_top" name="fulltext" className="form-control" />
          </form>
        </div>
      )
    }

  }
});