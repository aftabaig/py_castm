
function onError(e) {
  console.log(e);
}

// Create CastM module.
var castM = angular.module('castM', ['ngResource', 'ui.router', 'ngStorage', 'ui.bootstrap', 'cgBusy']);

castM.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('^^');
  $interpolateProvider.endSymbol('^^');
});

castM.config(['$httpProvider', '$stateProvider', '$urlRouterProvider', function($httpProvider, $stateProvider, $urlRouterProvider) {

    $stateProvider
    .state('login', {
        url:'/login',
        templateUrl: "static/js/app/views/login.html",
        controller: "LoginController",
        resolve: {

        }
    })
    .state('casting', {
        templateUrl: "static/js/app/views/casting/base.html",
        abstract: true
    })
    .state('casting.home', {
        url: '/home',
        parent: 'casting',
        templateUrl: 'static/js/app/views/casting/home.html'
        controller: 'HomeController',
        resolve: {
            profile: function(UserService) {
                return UserService.profile()
            }
        }
    })
    .state('event.links', {
        url:'/events/:eventId/links',
        parent: 'casting',
        templateUrl: 'static/js/app/views/casting/links.html'
        controller: 'LinksController',
        resolve: {
            event: function($stateParams, EventService) {
                return EventService.eventDetail($stateParams.eventId);
            },
            talentAttendees: function($stateParams, EventService) {
                return EventService.allTalentAttendees($stateParams.eventId);
            },
            castingAttendees: function($stateParams, EventService) {
                return EventService.allCastingAttendees($stateParams.eventId);
            }
        }
    })
    .state('event.schedules', {
        url: '/events/:eventId/schedules.html'
    })

}

castM.config(function($routeProvider) {
    $routeProvider
        .when("/login", {
            templateUrl: 'static/js/app/views/login.html',
            controller: 'LoginController',
            resolve: {

            }
        })
        .when("/home", {
            templateUrl: static/js/app/views/casting_home.html",
            controller: "HomeController",
            resolve: {
                profile: function($route, UserService) {
                    return UserService.profile()
                }
            }
        })
        .when("/events/:eventId/links", {
            templateUrl: "static/js/app/views/links.html",
            controller: "LinksController",
            resolve: {
                event: function($route, EventService) {
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
        .when("/events/:eventId/schedules", {
            templateUrl: "static/js/app/views/schedules.html",
            controller: "ScheduleController",
            resolve: {
                event: function($route, EventService) {
                    return EventService.eventDetail($route.current.params.eventId);
                },
                schedules: function($route, ScheduleService) {
                    return ScheduleService.getSchedules($route.current.params.eventId);
                },
                talentAttendees: function($route, EventService) {
                    return EventService.approvedTalentAttendees($route.current.params.eventId);
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