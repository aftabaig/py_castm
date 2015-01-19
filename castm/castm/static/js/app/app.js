
function onError(e) {
  console.log(e);
}

// Create CastM module.
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
        .when("/home", {
            templateUrl: "static/js/app/views/home.html",
            controller: "HomeController",
            resolve: {
                profile = function($route, UserService) {
                    return UserService.profile()
                }
            }
        })
        .when("/events/:eventId/links", {
            templateUrl: "static/js/app/views/links.html",
            controller: "LinksController",
            resolve: {
                event = function($route, EventService) {
                    return EventService.eventDetail($route.current.params.eventId);
                },
                talentAttendees: function($route, EventService) {
                    return EventService.allTalentAttendees($route.current.params.eventId);
                },
                castingAttendees: function($route, EventService) {
                    return EventService.allCastingAttendees($route.current.params.eventId);
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