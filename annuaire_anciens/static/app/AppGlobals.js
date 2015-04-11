module.exports =    {   url:    {   autocomplete:   {   fulltext:  '/api/v1/autocomplete/fulltext'
                                                    },
                                    search:         {   fulltext:   '/api/v1/ancien'
                                                    },
                                    ancien:         function(id) { return '/api/v1/ancien/'+ id; },
                                    ancien_complet: function(id) { return '/api/v1/ancien/'+ id +'?complet=True'; },
                                    photo:          function(photo_id)
                                                    {
                                                        if(photo_id)
                                                            return "/static/img/" + photo_id;
                                                        else
                                                            return "/static/img/no_photo.jpg";
                                                    },
                                    user:           {   experience:     {       setPrimaire:    function(id)    { return "/api/v1/me/experience/" + id + "/set_default"; },
                                                                                update:         function(id)    { return "/api/v1/me/experience/" + id; }
                                                                        }
                                                    },
                                    logged:         '/api/v1/logged',
                                    login:          '/api/v1/login',
                                    logout:         '/api/v1/logout',
                                    whoami:         '/api/v1/me'
                                }
};