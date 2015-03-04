
function onError(e) {
  console.log(e);
}

// Create CastM module.
var castM = angular.module('castM', ['ngResource', 'ui.router', 'ui.calendar', 'ui.bootstrap', 'ngStorage', 'cgBusy']);


castM.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('^^');
  $interpolateProvider.endSymbol('^^');
});

castM.filter('startFrom', function() {
    return function(input, start) {
        start = +start;
        return input.slice(start);
    }
});


castM.config(function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise("/login");

    $stateProvider
    .state('error', {
        url:'/error',
        resolve: {
            error: function() {
                return this.self.error;
            }
        },
        templateUrl: "static/js/app/views/error.html",
        controller: "ErrorController"
    })
    .state('login', {
        url:'/login',
        templateUrl: "static/js/app/views/login.html",
        controller: "LoginController"
    })
    .state('logout', {
        url: '/logout',
        controller: function($scope, $location, $localStorage) {
            delete $localStorage.user;
            $location.path("/login");
        }
    })
    .state('casting', {
        templateUrl: "static/js/app/views/casting/base.html",
        abstract: true,
        controller: function($scope, profile, headshots, myEvents) {
            $scope.profile = profile;
            if (headshots && headshots.length > 0) {
                $scope.headshot = headshots[0];
            }
            else {
                $scope.headshot = {}
            }
            $scope.showOrganization = false;
            $scope.showEvents = false;
            if (myEvents && myEvents.length > 0) {
                $scope.myEvent = myEvents[0];
            }
            $scope.toggleMyOrganization = function() {
                $scope.showOrganization = !$scope.showOrganization;
                $scope.showEvents = false;
            }
            $scope.toggleMyEvents = function() {
                $scope.showOrganization = false;
                $scope.showEvents = !$scope.showEvents;
            }
        },
        resolve: {
            profile: function(UserService) {
                return UserService.profile();
            },
            headshots: function(UserService) {
                return UserService.headshots();
            },
            myEvents: function(EventService) {
                return EventService.myEvents();
            }
        }
    })
    .state('casting.event', {
        views: {
            'info': {
                templateUrl: "static/js/app/views/casting/event/info.html"
            },
            '': {
                templateUrl: "static/js/app/views/casting/event/base.html"
            }
        },
        abstract: true,
        parent: 'casting'
    })
    .state('casting.organization', {
        views: {
            'info': {
                templateUrl: "static/js/app/views/casting/organization/info.html"
            },
            '': {
                templateUrl: "static/js/app/views/casting/organization/base.html"
            }
        },
        abstract: true,
        parent: 'casting'
    })
    .state('casting.organization.home', {
        url: '/home',
        parent: 'casting.organization',
        templateUrl: 'static/js/app/views/casting/organization/home.html',
        controller: 'HomeController'
    })
    .state('casting.organization.forms', {
        url: '/organizations/:organizationId/forms',
        parent: 'casting.organization',
        templateUrl: 'static/js/app/views/casting/organization/rating-form.html',
        controller: 'RatingFormController',
        resolve: {
            fields: function($stateParams, RatingService) {
                return RatingService.formFields($stateParams.organizationId);
            }
        }
    })
    .state('casting.event.talents', {
        url:'/events/:eventId/talents',
        parent: 'casting.event',
        templateUrl: 'static/js/app/views/casting/event/talent-attendees.html',
        controller: 'TalentAttendeesController',
        resolve: {
            event: function($stateParams, EventService) {
                return EventService.eventDetail($stateParams.eventId);
            },
            talentAttendees: function($stateParams, EventService) {
                return EventService.allTalentAttendees($stateParams.eventId);
            }
        }
    })
    .state('casting.event.casting', {
        url:'/events/:eventId/casting',
        parent: 'casting.event',
        templateUrl: 'static/js/app/views/casting/event/casting-attendees.html',
        controller: 'CastingAttendeesController',
        resolve: {
            event: function($stateParams, EventService) {
                return EventService.eventDetail($stateParams.eventId);
            },
            castingAttendees: function($stateParams, EventService) {
                return EventService.allCastingAttendees($stateParams.eventId);
            }
        }
    })
    .state('casting.event.sessions', {
        url: '/events/:eventId/sessions',
        parent: 'casting.event',
        templateUrl: 'static/js/app/views/casting/event/sessions.html',
        controller: 'SessionController',
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
    })
    .state('casting.event.schedule', {
        url: '/events/:eventId/schedule',
        parent: 'casting.event',
        templateUrl: 'static/js/app/views/casting/event/schedule.html',
        controller: 'ScheduleController',
        resolve: {
            event: function($stateParams, EventService) {
                return EventService.eventDetail($stateParams.eventId);
            },
            schedules: function($stateParams, ScheduleService) {
                return ScheduleService.getSchedules($stateParams.eventId);
            }
        }
    })
    .state('casting.event.callbacks', {
        url: '/events/:eventId/callbacks',
        parent: 'casting.event',
        templateUrl: 'static/js/app/views/casting/callbacks.html',
        controller: 'CallbackController',
        resolve: {
            event: function($stateParams, EventService) {
                return EventService.eventDetail($stateParams.eventId);
            },
            callbacks: function($stateParams, CallbackService) {
                return CallbackService.getCallbacks($stateParams.eventId);
            }
        }
    })
    .state('casting.event.broadcasting', {
        url: '/events/:eventId/broadcasting',
        templateUrl: 'static/js/app/views/casting/event/broadcasting.html',
        controller: 'BroadcastController',
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

});

castM.run(function($rootScope, $state) {
    $rootScope.$on('$stateChangeError', function(event, toState, toParams, fromState, fromParams, error) {
        console.log("ended");
        event.preventDefault();
        $state.get("error").error = error;
        return $state.go("error");
    });
});



// Directive for showing loading bar during state change.
castM.directive('routeLoader', function($rootScope) {
    return {
        link: function(scope, element) {
            element.addClass('ng-hide');
            var unRegister = $rootScope.$on('$stateChangeStart', function() {
                console.log("started")
                element.removeClass('ng-hide');
            });
            scope.$on('$destroy', unRegister);
        }
    };
});

castM.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
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