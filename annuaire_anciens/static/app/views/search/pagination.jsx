/**
 * @jsx React.DOM
 */
var PaginationBlock = React.createClass({
    handleClick:function(e){
        e.preventDefault();
        if(!this.props.disabled) {
            this.props.handleClick(this.props.page);
        }
    },
    render: function(){
        if(this.props.disabled) {
            return  <li className="disabled">
                        <span>{this.props.text}</span>
                    </li>;
        }else if(this.props.active){
            return  <li className="active">
                        <span>{this.props.text}</span>
                    </li>;
        } else {
            return <li><a href="#" onClick={this.handleClick}>{this.props.text}</a></li>
        }
    }
});

module.exports = React.createClass({
        getPageList: function(page, max_page) {
            var delta = 2;      // nombre de pages à afficher autour de la page en cours

            var pages = [];
            for (var i = delta; i > 0; i--) {
                var temppage = page - i;
                if (temppage > 0) {
                    pages.push(temppage);
                }
            }
            pages.push(page);
            for (var j = 1; j <= delta; j++) {
                var pagetemp = page + j;
                if (pagetemp <= max_page) {
                    pages.push(pagetemp);
                }
            }

            return pages;
        },
        buildPaginationBlocks: function(current_page, max_page){
            var changePage = this.props.handlePaginationClick;

            var pages = this.getPageList(current_page, max_page);

            var pagination_blocks = [];
            if(current_page == 1) {
                pagination_blocks.push(<PaginationBlock disabled={true} text="&lt;&lt;" />);
                pagination_blocks.push(<PaginationBlock disabled={true} text="&lt;" />);
            } else {
                pagination_blocks.push(<PaginationBlock disabled={false} text="&lt;&lt;" page={1} handleClick={changePage} />);
                pagination_blocks.push(<PaginationBlock disabled={false} text="&lt;" page={current_page-1} handleClick={changePage} />);
            }

            if(!pages.some(function(p){ return p == 1; })) {
                pagination_blocks.push(<PaginationBlock disabled={true} text="..." />);
            }

            pages.forEach(
                function(p)
                {
                    if(p == current_page) {
                        pagination_blocks.push(<PaginationBlock active={true} text={p} />);
                    } else {
                        pagination_blocks.push(<PaginationBlock disabled={false} text={p} page={p} handleClick={changePage} />);
                    }
                }
            );

            if(!pages.some(function(p){ return p == max_page; })) {
                pagination_blocks.push(<PaginationBlock disabled={true} text="..." />);
            }

            if(current_page == max_page) {
                pagination_blocks.push(<PaginationBlock disabled={true} text="&gt;" />);
                pagination_blocks.push(<PaginationBlock disabled={true} text="&gt;&gt;" />);
            } else {
                pagination_blocks.push(<PaginationBlock disabled={false} text="&gt;" page={current_page+1} handleClick={changePage} />);
                pagination_blocks.push(<PaginationBlock disabled={false} text="&gt;&gt;" page={max_page} handleClick={changePage} />);
            }
            
            return pagination_blocks;
        },
        render: function() {

            if (this.props.max_page > 1) {
                var pagination_blocks = this.buildPaginationBlocks(this.props.page, this.props.max_page);
                return  <div className="col-md-12 text-center">
                            <ul className="pagination">
                                {pagination_blocks}
                            </ul>
                        </div>;
            } else {
                return <div className="col-md-12 text-center"></div>;
            }


        }

    }
);