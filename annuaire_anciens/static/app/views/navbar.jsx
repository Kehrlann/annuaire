/**
  * @jsx React.DOM
  */

var Popover = require('./helpers/popover.jsx');

module.exports = React.createClass({

  getInitialState: function(){
    return {
      isUserConnected: false,
      isSearchPage: false,
      showLoginBox: false
    }
  },

  componentDidMount: function(){
    var _this = this;
    $(this.refs['openLoginBtn'].getDOMNode()).popover({
        html : true,
        placement: "bottom",
        content: function() {
          return $(_this.refs['loginPopover'].getDOMNode()).html();
        }
    });
  },

  handleLogin: function(){

  },

  handleOpenLogin: function(e) {
      e.preventDefault();
      // Toggle popover visibility
      this.setState({showLoginBox: !this.state.showLoginBox});
  },

  render : function() {

    var popoverContent = (
      <div role="form" className="form">
        <div className="form-group">
          <label htmlFor="mail">Adresse email</label>
          <input type="email" className="form-control" ref="email" placeholder="Enter email"/>
        </div>
        <div className="form-group">
          <label htmlFor="password">Mot de passe</label>
          <input type="password" className="form-control" ref="password" placeholder="Password"/>
        </div>
        <div className="checkbox">
          <label>
            <input type="checkbox" ref="rememberme" defaultChecked /> Se souvenir de moi
          </label>
        </div>
        <div className="error"></div>
        <button type="submit" className="btn btn-default" onClick={this.handleLogin} >Valider</button>
        <a href="#" style={{marginLeft: "10px"}} ><img src="img/linkedin.gif"/></a>
        <a className="btn btn-link" onClick={this.handleOpenLogin}>Annuler</a>
      </div>
    );

    return (
      <Popover
              content={popoverContent}
              placement="bottom"
              visible={this.state.visible}>
          <button ref="openLoginBtn" className="btn btn-default navbar-btn" onClick={this.handleOpenLogin}>
            <span className="glyphicon glyphicon-log-out"></span> Se connecter
          </button>
      </Popover>
    );
  }
});