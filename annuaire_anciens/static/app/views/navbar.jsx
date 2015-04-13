/**
 * @jsx React.DOM
 */

var LoginView   =   require('./login.jsx');
var appGlobals  =   require('../helpers/AppGlobals.js');
var cookie      =   require('../helpers/cookies.js');

module.exports = React.createClass({

    getInitialState: function () {
        return {
            isUserConnected: false,
            isSearchPage: false
        }
    },
    handleSearch: function (e) {
        // TODO : add autocomplete
    },
    componentDidMount: function(){
        $.ajax(
            {
                method: "GET",
                url: appGlobals.url.logged,
                success: function (data) {
                    var results = eval("(" + data + ")");
                    this.setState( {isUserConnected: results.logged});
                }.bind(this)
            }
        );
    },
    handleLogin: function (isLoggedIn) {
        console.log("Navbar caught login", isLoggedIn);
        this.setState({isUserConnected: isLoggedIn});
        Backbone.history.navigate("/login", {trigger: true});
    },
    handleLogout: function(e){
        e.preventDefault();
        $.ajax(
            {
                method: "GET",
                url: appGlobals.url.logout,
                success: function (data) {
                    this.setState( {isUserConnected: false});
                    Backbone.history.navigate("/logout", {trigger: true});
                }.bind(this)
            }
        );
    },
    clickMonCompte: function(e){
        e.preventDefault();
        Backbone.history.navigate("/ancien/"+cookie.getIdAncien(), {trigger:true});
    },
    clickHome: function(e){
        e.preventDefault();
        Backbone.history.navigate("/", {trigger:true});
    },
    render: function () {

        if (!this.state.isUserConnected) {
            return (
                <div className="col-lg-10 col-lg-offset-1">
                    <div className="navbar-right" id="js-navbar">
                        <LoginView onLogin={this.handleLogin}></LoginView>
                    </div>
                </div>
            );
        }
        else {
            return (
                <div className="col-lg-10 col-lg-offset-1">
                    <a className="navbar-brand" href="#" onClick={this.clickHome}>Mines-Alumni.com</a>

                    <div className="navbar-right" id="js-navbar">
                        <div className="nav navbar-nav navbar-right">
                            <a className='btn btn-default navbar-btn hidden-xs' href="#" onClick={this.clickMonCompte}>Mon compte</a>
                            <a className='btn btn-link navbar-btn hidden-xs' href="#" onClick={this.handleLogout}>D&eacute;connexion</a>
                            <a className='btn btn-default navbar-btn visible-xs' href="#">
                                <span className="glyphicon glyphicon-user"></span>
                            </a>
                            <a className='btn btn-danger navbar-btn visible-xs' href="#">
                                <span className="glyphicon glyphicon-log-out"></span>
                            </a>
                        </div>
                        <form className="navbar-form navbar-left nav-search-zone" role="search">
                            <span className="glyphicon glyphicon-search"></span>
                            <input type="text" autoComplete="off" ref="fulltext_top" onKeyUp={this.handleSearch} name="fulltext" className="form-control" />
                        </form>
                    </div>
                </div>
            )
        }

    }
});