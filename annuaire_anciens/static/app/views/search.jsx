/**
  * @jsx React.DOM
  */

module.exports = React.createClass({

  getInitialState: function(){
    return {}
  },

  handleAdvancedSearch: function(e){

  },

  render : function() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-lg-10 col-lg-offset-1">
            <div className="main-search-field">
              <form>
                <input type="text" className="form-control input-lg" ref="searchBar" />
                <span className="glyphicon glyphicon-search"></span>
              </form>
            </div>
            <a href="#" onClick={this.handleAdvancedSearch} className="pull-right btn btn-link">Recherche avancée</a>
          </div>
        </div>
      </div> );
  }
});