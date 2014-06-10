var casper = require('casper').create();
var fs = require('fs');


function savePageToFile(){
  // TODO: remove feedback panel (.feedback-panel)
  casper.evaluate(clean_up);
  fs.write(destination+target, casper.getPageContent(), 'w');
}

var links = [];

var idAndEntreprise = casper.cli.args[0]; // looks like 13|Snecma
var split = idAndEntreprise.split('|');
var id = split[0];
var entreprise = split[1].replace(/ /g, '+'); // replace all the spaces with "+"

casper.start('http://www.societe.com/cgi-bin/mainsrch?champ='+entreprise, function() {

  casper.echo("Got to results page");

  // Is there a perfect match?
  if(casper.getPageContent().indexOf('correspond exactement') > -1){
    // casper.echo('There is a perfect match');
    // Get the first link
    var companyPage = casper.evaluate(function(){
      var linkNode = document.querySelector('[href*="/societe/"]');
      if(linkNode){
        return linkNode.href;
      }
      else{
        return null;
      }
    });

    if(companyPage){
      casper.echo(id+'|'+companyPage);
    }
    else{
      casper.echo(id+'|ERROR');
    }

  }
  else{
    casper.echo(id+'|ERROR');
  }

});

casper.run(function(){
  this.exit();
});