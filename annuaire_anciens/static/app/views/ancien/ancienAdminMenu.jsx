/**
 * @jsx React.DOM
 */

module.exports = React.createClass({
    render:function()
    {
        return <div className="row custom-ancien-container-light experience-container" id="management">
            <div className="experience container">
                <div className="row">
                    <div className="col-sm-1 custom-text-center-big-screen">
                        <a className="btn btn-success" type="button" >
                            <i className="glyphicon glyphicon-lock"></i>
                        </a>
                    </div>
                    <div className="col-sm-11 admin-label" >
                        Modifier mon mot de passe
                    </div>
                </div>
                <div className="row admin-small-row" >
                    <div className="col-sm-1 custom-text-center-big-screen">
                        <a className="btn btn-success" type="button" onClick={this.props.addExperience}>
                            <i className="glyphicon glyphicon-plus"></i>
                        </a>
                    </div>
                    <div className="col-sm-11 admin-label" >
                        Ajouter une expérience professionnelle à ma fiche ancien
                    </div>
                </div>
                <div className="row admin-small-row" >
                    <div className="col-sm-1 custom-text-center-big-screen">
                        <a className="btn btn-primary" type="button" >
                            <i className="glyphicon glyphicon-pushpin"></i>
                        </a>
                    </div>
                    <div className="col-sm-11 admin-label">
                        Associer mon compte LinkedIn (lien vers LinkedIn dans ma fiche ancien)
                    </div>
                </div>
                <div className="row admin-small-row" >
                    <div className="col-sm-1 custom-text-center-big-screen">
                        <a className="btn btn-danger" type="button" >
                            <i className="glyphicon glyphicon-remove"></i>
                        </a>
                    </div>
                    <div className="col-sm-11 admin-label">
                        Dissocier mon compte LinkedIn (lien vers LinkedIn dans ma fiche ancien)
                    </div>
                </div>
                <div className="row admin-small-row" >
                    <div className="col-sm-1 custom-text-center-big-screen">
                        <a className="btn btn-primary" type="button" >
                            <i className="glyphicon glyphicon-cloud-download"></i>
                        </a>
                    </div>
                    <div className="col-sm-11 admin-label">
                        Importer des expériences depuis LinkedIn
                    </div>
                </div>
                <div className="row admin-small-row" >
                    <div className="col-sm-1 custom-text-center-big-screen">
                        <a className="btn btn-danger" type="button" >
                            <i className="glyphicon glyphicon-eye-close"></i>
                        </a>
                    </div>
                    <div className="col-sm-11 admin-label">
                        Cacher ma fiche ancien dans l'annuaire
                    </div>
                </div>
                <div className="row admin-small-row" >
                    <div className="col-sm-1 custom-text-center-big-screen">
                        <a className="btn btn-success" type="button" >
                            <i className="glyphicon glyphicon-eye-open"></i>
                        </a>
                    </div>
                    <div className="col-sm-11 admin-label">
                        Rendre ma fiche ancien visible dans l'annuaire
                    </div>
                </div>
            </div>
        </div>;
    }
});