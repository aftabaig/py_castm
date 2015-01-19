
function onError(e) {
  console.log(e);
}

// Create module.
var castM = angular.module('castM', ['ngResource', 'ngRoute', 'ngStorage', 'ui.bootstrap', 'cgBusy']);

castM.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('^^');
  $interpolateProvider.endSymbol('^^');
});

castM.config(function($routeProvider) {
    $routeProvider
        .when("/login", {
            templateUrl: "static/js/app/views/login.html",
            controller: "LoginController",
            resolve: {

            }
        })
        .when("/events/:eventId/links", {
            templateUrl: "static/js/app/views/links.html",
            controller: "LinksController",
            resolve: {
                qualifiedTalentAttendees: function($route, EventService) {
                    return EventService.qualifiedTalentAttendees($route.current.params.eventId);
                },
                qualifiedCastingAttendees: function($route, EventService) {
                    return EventService.qualifiedCastingAttendees($route.current.params.eventId);
                },
                pendingTalentAttendees: function($route, EventService) {
                    return EventService.pendingTalentAttendees($route.current.params.eventId);
                },
                pendingCastingAttendees: function($route, EventService) {
                    return EventService.pendingCastingAttendees($route.current.params.eventId);
                }
            }
        })
        .otherwise({
            redirectTo: "/login"
        });
});


castM.directive('ngEnter', function () {
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