/**
 * @jsx React.DOM
 */
var appGlobals = require('../../AppGlobals.js');

module.exports = React.createClass({
        handleSubmit: function (e) {
            e.preventDefault();
            var input = $("#mainSearchBar");
            input.autocomplete('close');
            this.props.handleSearch(input.val(), 1);
        },
        componentDidMount: function () {
            var searchFullText = this.props.handleSearch;
            $("#mainSearchBar").autocomplete({
                source: appGlobals.url.autocomplete.fulltext,
                max: 10,
                delay: 50,
                cacheLength: 1,
                scroll: false,
                select: function (event, ui) {
                    $(this).val(ui.item.value);
                    var query = ui.item.value;
                    searchFullText(query, 1);
                }
            });
        },
        render: function () {
            return  <div className="main-search-field">
                        <form onSubmit={this.handleSubmit}>
                            <input type="text" className="form-control input-lg" ref="searchBar" id="mainSearchBar" />
                            <span className="glyphicon glyphicon-search"></span>
                        </form>
                    </div>;
        }
    }
);