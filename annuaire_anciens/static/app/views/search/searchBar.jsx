/**
 * @jsx React.DOM
 */

module.exports = React.createClass({
        handleSubmit: function (e) {
            e.preventDefault();
            this.props.handleSearch($("#mainSearchBar").val(), 1);

            // TODO
            // TODO
            // TODO
            // TODO
            // TODO
            // TODO
            // TODO
            // TODO
            // TODO
            // close autocomplete
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