/**
 * @jsx React.DOM
 */
var SearchResultList = require('./searchResultList.jsx');
var SearchBar = require('./searchBar.jsx');
var Pagination = require('./pagination.jsx');
var appGlobals = require('../../AppGlobals.js');


module.exports = React.createClass({

    getInitialState: function () {
        return {    query:  null,
                    page:   1,
                    max_page: 1,
                    anciens: []
                }
    },
    handleAdvancedSearch: function (e) {

    },
    changePage: function(p){
        this.searchFullText(this.state.query, p);
    },
    componentDidMount: function(){
    },
    searchFullText: function(query, page){
        this.state.query = query;
        this.state.page = page;
        $.ajax(
            {
                method:     "GET",
                //url: appGlobals.url.search.fulltext + "?q=" + encodeURIComponent(query) + "&p=" + page,
                url:        appGlobals.url.search.fulltext,
                data:       { q : encodeURIComponent(query), p : page },
                success:    function (data)
                            {
                                var results = eval("(" + data + ")");
                                this.setState( {anciens: results.data, query: query, page: page, max_page : results.max_pages});
                            }.bind(this)
            }
        );
    },
    render: function () {
        return (
            <div className="container">
                <div className="row">
                    <div className="col-lg-10 col-lg-offset-1">
                        <SearchBar handleSearch={this.searchFullText}/>
                        <a href="#" onClick={this.handleAdvancedSearch} className="pull-right btn btn-link">Recherche avancée</a>
                    </div>
                </div>
                <div className="row" style={{ marginTop: "10px"}}>
                    <Pagination page={this.state.page} max_page={this.state.max_page} handlePaginationClick={this.changePage} />
                </div>
                <div className="row" style={{ marginTop: "10px"}}>
                    <SearchResultList anciens={this.state.anciens} />
                </div>
            </div> );
    }
});