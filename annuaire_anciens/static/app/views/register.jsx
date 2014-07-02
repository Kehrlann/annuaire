/**
  * @jsx React.DOM
  */

module.exports = React.createClass({

  getInitialState: function(){
    return {
      isEmailSet: false,
      isPasswordSet: false
    }
  },

  handleEmailKeyUp: function(e){
    console.log("handleEmailKeyUp");
    if(e.target.value.length > 4){
      console.log("email is set");
      this.setState({ isEmailSet: true });
    }
  },

  handleEmailBlur: function(e){
    if(e.target.value.length == 0){
      this.setState({ isEmailSet: false });
    }
  },

  handlePasswordKeyUp: function(e){
    if(e.target.value.length > 5){
      this.setState({ isPasswordSet: true });
    }
  },

  handlePasswordBlur: function(e){
    if(e.target.value.length == 0){
      this.setState({ isPasswordSet: false });
    }
  },

  handleSubmit: function(){

  },

  render : function() {
    return (
      <div className="container">
        <div className="row" style={{paddingTop: "40px"}}>
          <div className="col-lg-10 col-lg-offset-1">
            <div className="fadein">
              <h4 style={{paddingBottom: "10px"}}>1. Je prouve que je suis bien un ancien des Mines</h4>
              <div className="row">
                <div className="col-md-12 auth-option">
                  <form className="form form-inline">
                    <div className="row">
                        <div className="col-sm-6">
                            <div className="row">
                                <div className="form-group col-xs-6" style={{paddingRight: "1px"}}>
                                    <input type="text" ref="email" className="form-control" placeholder="prenom.nom" onKeyUp={this.handleEmailKeyUp} onBlur={this.handleEmailBlur} />
                                </div>
                                <div className="form-group col-xs-6" style={{paddingLeft: "1px"}}>
                              <select ref="domain" className="form-control">
                                  <option value="@mines-paris.org">@mines-paris.org</option>
                                  <option value="@mines-saint-etienne.org">@mines-saint-etienne.org</option>
                                  <option value="@mines-nancy.org">@mines-nancy.org</option>
                              </select>
                            </div>
                        </div>
                      </div>
                    </div>
                    <span className="help-block">Un email sera envoyé à cette adresse pour vérification. </span>
                    <div className={this.state.isEmailSet?"fadein":"invisible"}>
                      <h4 style={{paddingTop: "40px", paddingBottom: "10px"}}>2. Je choisis un mot de passe pour les fois prochaines</h4>
                      <div className="row">
                        <div className="col-sm-6">
                          <input type="password" className="form-control" ref="password" placeholder="Mot de passe" onKeyUp={this.handlePasswordKeyUp} onBlur={this.handlePasswordBlur} />
                        </div>
                      </div>
                      <span className="help-block">Ce mot de passe servira pour me connecter à Mines-Alumni.com</span>
                      <div style={{paddingTop: "40px"}} className={this.state.isPasswordSet?"fadein":"invisible"}>
                        <button type="submit" className="btn btn-default" onClick={this.handleSubmit}>Je Valide</button>
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
});