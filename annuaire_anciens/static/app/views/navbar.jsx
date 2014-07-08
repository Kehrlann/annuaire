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
      hasError: false,
      isLoading: false
    }
  },

  handleLogin: function(e){
    // prevent the form from posting
    e.preventDefault();
    form = $(e.target);
    var _this = this;

    this.setState({isLoading: true});
    $.ajax({
      type: "POST",
      url: "/login",
      data: form.serialize(),
      success: function(data, response, qsq){
        console.log("Success", data, response, qsq);
        _this.setState({isLoading: false})
        // window.location.replace(data);
      },
      error: function(){
        console.log("Failure");
        _this.setState({hasError: true, isLoading: false});
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
      <form ref="loginForm" role="form" className="form" onSubmit={this.handleLogin}>
        <div className="form-group">
          <label htmlFor="mail">Adresse email</label>
          <input type="email" className="form-control" name="mail" placeholder="Enter email"/>
        </div>
        <div className="form-group">
          <label htmlFor="password">Mot de passe</label>
          <input type="password" className="form-control" name="password" placeholder="Password"/>
        </div>
        <div className="checkbox">
          <label>
            <input type="checkbox" name="rememberme" defaultChecked /> Se souvenir de moi
          </label>
        </div>
        <div className="loading hidden">
          Chargement...
        </div>
        <div className="error">
          <div className="alert alert-danger hidden">
            Merci de bien vouloir réessayer.
          </div>
        </div>
        <button type="submit" className="btn btn-default">Valider</button>
        <a href="#" style={{marginLeft: "10px"}} ><img src="img/linkedin.gif"/></a>
        <a className="btn btn-link" onClick={this.handleOpenLogin}>Annuler</a>
      </form>
    );

    return (
      <Popover
              content={popoverContent}
              placement="bottom"
              visible={this.state.showLoginBox}
              hasError={this.state.hasError}
              isLoading={this.state.isLoading}>
          <button className="btn btn-default navbar-btn" onClick={this.handleOpenLogin}>
            <span className="glyphicon glyphicon-log-out"></span> Se connecter
          </button>
      </Popover>
    );
  }
});