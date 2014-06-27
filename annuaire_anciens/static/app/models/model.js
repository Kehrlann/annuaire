module.exports = Backbone.Model.extend({

  url: function() {
    return '/api/model/' + this.id;
  },

  initialize: function(params) {

  }

});