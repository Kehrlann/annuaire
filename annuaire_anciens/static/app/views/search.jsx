/**
 * @jsx React.DOM
 */
window.$ = require('jquery');
module.exports = React.createClass({

    getInitialState: function () {
        return {}
    },

    handleAdvancedSearch: function (e) {

    },
    componentDidMount: function() {
        var reactComp = this;
        $("#mainSearchBar").autocomplete({
            source : appGlobals.url.autocomplete.fulltext,
            max: 10,
            delay: 50,
            cacheLength: 1,
            scroll: false,
            select: function(event, ui) {
                Backbone.$(this).val(ui.item.value);
                var query = ui.item.value;
                console.log("~~~~~~~~~~~~~~~~~~~~~~~~~~> Autocomplete");
                console.log(ui.item.value);
                console.log(query);
            }
        });
    },
    render: function () {
        return (
            <div className="container">
                <div className="row">
                    <div className="col-lg-10 col-lg-offset-1">
                        <div className="main-search-field">
                            <form>
                                <input type="text" className="form-control input-lg" ref="searchBar" id="mainSearchBar" />
                                <span className="glyphicon glyphicon-search"></span>
                            </form>
                        </div>
                        <a href="#" onClick={this.handleAdvancedSearch} className="pull-right btn btn-link">Recherche avancée</a>
                    </div>
                </div>
            </div> );
    }
});