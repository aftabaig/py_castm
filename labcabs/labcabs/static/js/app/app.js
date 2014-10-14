
function onError(e) {
  console.log(e);
}

// Create module.
var lc = angular.module('lc', ['ngResource', 'ngRoute', 'ngStorage', 'datePicker', 'ui.bootstrap', 'cgBusy']);

lc.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('^^');
  $interpolateProvider.endSymbol('^^');
});

lc.config(function($routeProvider) {
    $routeProvider
        .when("/login", {
            templateUrl: "static/js/app/views/login.html",
            controller: "LoginController",
            resolve: {

            }
        })
        .when("/entities", {
            templateUrl: "static/js/app/views/entities.html",
            controller: "EntitiesController",
            resolve: {
                entities: function (EntityService) {
                    return EntityService.all();
                }
            }
        })
        .when("/entities/new/", {
            templateUrl: "static/js/app/views/entity.html",
            controller: "EntityController",
            resolve: {
                entity: function() {
                    return null;
                }
            }
        })
        .when("/entities/:id/", {
            templateUrl: "static/js/app/views/entity.html",
            controller: "EntityController",
            resolve: {
                entity: function($route, EntityService) {
                    var entityId = $route.current.params.id;
                    return EntityService.info(entityId);
                }
            }
        })
        .when("/consignments/", {
            templateUrl: "static/js/app/views/consignments.html",
            controller: "ConsignmentsController",
            resolve: {
                consignments: function($route, ConsignmentService) {
                    return ConsignmentService.all();
                }
            }
        })
        .when("/consignments/new/", {
            templateUrl: "static/js/app/views/consignment.html",
            controller: "ConsignmentController",
            resolve: {
                consignment: function() {
                    return null;
                },
                entities: function(EntityService) {
                    return EntityService.all();
                }
            }
        })
        .when("/consignments/:id/", {
            templateUrl: "static/js/app/views/consignment.html",
            controller: "ConsignmentController",
            resolve: {
                consignment: function($route, ConsignmentService) {
                    var consignmentId = $route.current.params.id;
                    return ConsignmentService.info(consignmentId);
                },
                entities: function(EntityService) {
                    return EntityService.all();
                }
            }
        })
        .when("/search", {
            templateUrl: "static/js/app/views/search.html",
            controller: "SearchController",
            resolve: {
                consignments: function(ConsignmentService) {
                    return ConsignmentService.all();
                },
                entities: function(EntityService) {
                    return EntityService.all();
                }
            }
        })
        .otherwise({
            redirectTo: "/entities"
        });
});

lc.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEnter);
                });

                event.preventDefault();
            }
        });
    };
});