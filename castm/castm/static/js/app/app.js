
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
        url: '/events/:eventId/schedules',
        parent: 'casting',
        templateUrl: 'static/js/app/views/casting/schedules.html',
        controller: 'ScheduleController',
        resolve: {
            event: function($stateParams, EventService) {
                return EventService.eventDetail($stateParams.eventId);
            },
            schedules: function($stateParams, ScheduleService) {
                return ScheduleService.getSchedules($stateParams.eventId);
            },
            talentAttendees: function($stateParams, EventService) {
                return EventService.approvedTalentAttendees($stateParams.eventId);
            }
        }
    });


}

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