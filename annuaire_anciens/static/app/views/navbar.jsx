/**
  * @jsx React.DOM
  */

var Popover = require('./helpers/popover.jsx');

module.exports = React.createClass({

  getInitialState: function(){
    return {
      isUserConnected: false,
      isSearchPage: false,
      showLoginBox: false,
      hasError: false
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
    var form = $(this.refs['loginForm'].getDOMNode());
    var _this = this;
    $.ajax({
      type: "POST",
      url: "/login",
      data: form.serialize(),
      success: function(data){
        console.log("Success : "+data);
        // window.location.replace(data);
      },
      error: function(){
        _this.setState({hasError: true});
      }
    });
  },

  handleOpenLogin: function(e) {
    e.preventDefault();
    // Toggle popover visibility
    this.setState({showLoginBox: !this.state.showLoginBox});
  },

  render : function() {

    var popoverContent = (
      <form ref="loginForm" role="form" className="form">
        <div className="form-group">
          <label htmlFor="mail">Adresse email</label>
          <input type="email" className="form-control" placeholder="Enter email"/>
        </div>
        <div className="form-group">
          <label htmlFor="password">Mot de passe</label>
          <input type="password" className="form-control" placeholder="Password"/>
        </div>
        <div className="checkbox">
          <label>
            <input type="checkbox" ref="rememberme" defaultChecked /> Se souvenir de moi
          </label>
        </div>
        <div className="error" style={this.state.hasError?{}:{display: "none"}}>
          <div className='alert alert-danger'>
            <button type='button' className='close' data-dismiss='alert'>&times;</button>Erreur de login !
          </div>
        </div>
        <button type="submit" className="btn btn-default" onClick={this.handleLogin} >Valider</button>
        <a href="#" style={{marginLeft: "10px"}} ><img src="img/linkedin.gif"/></a>
        <a className="btn btn-link" onClick={this.handleOpenLogin}>Annuler</a>
      </form>
    );
    return (
      <Popover
              content={popoverContent}
              placement="bottom"
              visible={this.state.showLoginBox}>
          <button ref="openLoginBtn" className="btn btn-default navbar-btn" onClick={this.handleOpenLogin}>
            <span className="glyphicon glyphicon-log-out"></span> Se connecter
          </button>
      </Popover>
    );
  }
});