/**
 * @jsx React.DOM
 */
module.exports.Simple = React.createClass({
        render: function()
                {
                    return  <div className="row" style={{marginBottom : "5px"}}>
                                <div className="col-sm-2 custom-text-right-big-screen cutsom-descriptor" style={{marginTop : "7px"}}>{this.props.label}</div>
                                <div className="col-sm-9">
                                    <input className="form-control" type="text" name={this.props.name} value={this.props.value} />
                                </div>
                            </div>;
                }
    }
);

module.exports.TextArea = React.createClass({
        render: function()
        {
            return  <div className="row" style={{marginBottom : "5px"}}>
                        <div className="col-sm-2 custom-text-right-big-screen cutsom-descriptor" style={{marginTop : "7px"}}>{this.props.label}</div>
                        <div className="col-sm-9">
                            <textarea rows="3" className="form-control" type="text" name={this.props.name} value={this.props.value} />
                        </div>
                    </div>;
        }
    }
);

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
            return  <div className="row" style={{marginBottom : "5px"}}>
                <div className="col-sm-2 custom-text-right-big-screen cutsom-descriptor" style={{marginTop : "7px"}}>{this.props.label}</div>
                <div className="col-sm-9">
                    <input className="form-control datepicker" type="text" name={this.props.name} value={this.props.value} autocomplete="off" />
                </div>
            </div>;
        }
    }
);