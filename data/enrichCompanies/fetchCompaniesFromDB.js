var pg = require('pg');
var _ = require('underscore');

var conString = "postgresql+psycopg2://localhost:5432/annuaire";

var client = new pg.Client(conString);
client.connect(function(err) {
  if(err) {
    return console.error('could not connect to postgres', err);
  }

  client.query("SELECT id_entreprise, nom FROM entreprise", function(err, result) {
    if(err) {
      return console.error('error running query', err);
    }

    result.rows.forEach(function(company){
      console.log(company.id_entreprise+"|"+company.nom);
    });


    client.end();
  });
});