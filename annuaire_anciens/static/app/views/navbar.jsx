/**
 * @jsx React.DOM
 */

var LoginView = require('./login.jsx');

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
        Backbone.history.navigate("/search", {trigger: true});
    },
    handleLogout: function(e){
        e.preventDefault();
        $.ajax(
            {
                method: "GET",
                url: appGlobals.url.logout,
                success: function (data) {
                    this.setState( {isUserConnected: false});
                    Backbone.history.navigate("/", {trigger: true});
                }.bind(this)
            }
        );
    },
    render: function () {

        if (!this.state.isUserConnected) {
            return (
                <LoginView onLogin={this.handleLogin}></LoginView>
            );
        }
        else {
            return (
                <div>
                    <div className="nav navbar-nav navbar-right">
                        <a className='btn btn-default navbar-btn hidden-xs' href="#">Mon compte</a>
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
            )
        }

    }
});