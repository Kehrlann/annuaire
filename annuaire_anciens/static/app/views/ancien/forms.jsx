/**
 * @jsx React.DOM
 */
var _formatError            =   function(error)
                                {
                                    return <li>{error}</li>;
                                };

var formatInputAndErrors    =   function(input, errors)
                                {
                                    var inputAndErrors = [];
                                    inputAndErrors.push(input);
                                    if (errors)
                                    {
                                        inputAndErrors.push(<ul className="help-block">{errors.map(_formatError)}</ul>);
                                    }
                                    return inputAndErrors;
                                };

var classesIfErrors         =   function(errors)
                                {
                                    return errors ? "row has-error" : "row";
                                };

module.exports.Simple = React.createClass(
    {
        render: function()
                {
                    var p = this.props;
                    return  <div className={classesIfErrors(p.errors)} style={{marginBottom : "5px"}}>
                                <label className="col-sm-2 custom-text-right-big-screen cutsom-descriptor control-label" style={{marginTop : "7px"}}>{p.label}</label>
                                <div className="col-sm-9">
                                    {   formatInputAndErrors(   <input className="form-control" type="text" name={p.name} defaultValue={p.value} />,
                                                                p.errors
                                                            )
                                    }
                                </div>
                            </div>;
                }
    }
);

module.exports.TextArea = React.createClass({
        render: function()
                {
                    var p = this.props;
                    return  <div className={classesIfErrors(p.errors)}  style={{marginBottom : "5px"}}>
                                <div className="col-sm-2 custom-text-right-big-screen cutsom-descriptor control-label" style={{marginTop : "7px"}}>{p.label}</div>
                                <div className="col-sm-9">
                                    {   formatInputAndErrors(   <textarea rows="3" className="form-control" type="text" name={p.name} defaultValue={p.value} />,
                                                                p.errors
                                                            )
                                    }
                                </div>
                            </div>;
                }
});

module.exports.Select = React.createClass({
        getOptions:     function ()
                        {
                            return this.props.options.map(function(value){ return <option value={value.value}>{value.name}</option>});
                        },
        render:         function ()
                        {
                            var p = this.props;
                            var options = this.getOptions();
                            return  <div className={classesIfErrors(p.errors)} style={{marginBottom : "5px"}}>
                                        <div className="col-sm-2 custom-text-right-big-screen cutsom-descriptor control-label" style={{marginTop : "7px"}}>{p.label}</div>
                                        <div className="col-sm-9">
                                            {   formatInputAndErrors(   <select className="form-control" type="text" name={p.name} defaultValue={p.value}>
                                                                            {options}
                                                                        </select>,
                                                                        p.errors
                                                                    )
                                            }
                                        </div>
                                    </div>;
                        }
});

module.exports.Date = React.createClass({
        componentDidMount: function(){
            $(".datepicker").each(
                function (index, value){
                    var date = $(this).val();
                    var dDate = new Date();
                    if(date!=""){
                        var dateArray = date.split("/");
                        dDate = new Date(dateArray[1], dateArray[0]-1, 1);
                    }
                    $(this).datepicker(
                        {
                            dateFormat:'mm/yy',
                            defaultDate:dDate
                        });
                }
            );

        },
        render: function()
        {
            var p = this.props;
            return  <div className={classesIfErrors(p.errors)} style={{marginBottom : "5px"}}>
                <div className="col-sm-2 custom-text-right-big-screen cutsom-descriptor control-label" style={{marginTop : "7px"}}>{p.label}</div>
                <div className="col-sm-9">
                    {   formatInputAndErrors(   <input className="form-control datepicker" type="text" name={p.name} defaultValue={p.value} autocomplete="off" />,
                                                p.errors
                                            )
                    }
                </div>
            </div>;
        }
    }
);