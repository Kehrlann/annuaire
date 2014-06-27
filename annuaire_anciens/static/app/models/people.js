//
// Dependencies
//
var Person = require('./person');

module.exports = Backbone.Collection.extend({

  model: Person,

  url: function() {
    // We will use a json fixture
    // Replace by actual url
    return '/app/fixtures/people.json';
  },

  initialize: function(params) {

  },

  parse: function(result){
    return result.people;
  }

});