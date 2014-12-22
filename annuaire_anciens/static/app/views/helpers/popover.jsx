/**
  * @jsx React.DOM
  */

module.exports = React.createClass({
    componentDidMount: function() {
        var $el = $(this.getDOMNode());

        $el.popover({
            react: true,
            title: this.props.title,
            content: this.props.content,
            trigger: 'manual',  // Don't toggle on click automatically
            placement: this.props.placement != null ?
                this.props.placement : undefined
        });
        if (this.props.visible) {
            $el.popover('show');
        }

        // window.popover = $el;
        window.popover = this;
    },

    componentDidUpdate: function(prevProps, prevState) {
        var $el = $(this.getDOMNode());

        var popoverId = $el.attr('aria-describedby');
        if(popoverId){
            if (prevProps.isLoading !== this.props.isLoading) {
                $('#'+popoverId+" .popover-content .loading").toggleClass('hidden', !this.props.isLoading);
            }

            if (prevProps.hasError !== this.props.hasError) {
                $('#'+popoverId+" .popover-content .alert").toggleClass('hidden', !this.props.hasError);
            }
        }

        if (prevProps.visible !== this.props.visible) {
            $el.popover(this.props.visible ? 'show' : 'hide');
        }
    },

    componentWillUnmount: function() {
        // Clean up before destroying: this isn't strictly
        // necessary, but it prevents memory leaks
        var $el = $(this.getDOMNode());
        var popover = $el.data('bs.popover');
        var $tip = popover.tip();
        React.unmountComponentAtNode(
            $tip.find('.popover-title')[0]
        );
        React.unmountComponentAtNode(
            $tip.find('.popover-content')[0]
        );
        $(this.getDOMNode()).popover('destroy');
    },

    render: function() {
        return this.props.children;
    }
});