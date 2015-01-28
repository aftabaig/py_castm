
function onError(e) {
  console.log(e);
}

// Create CastM module.
var castM = angular.module('castM', ['ngResource', 'ui.router', 'ngStorage', 'cgBusy']);

castM.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('^^');
  $interpolateProvider.endSymbol('^^');
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
    .state('casting', {
        templateUrl: "static/js/app/views/casting/base.html",
        abstract: true,
        controller: function($scope, profile, myEvents) {
            $scope.profile = profile;
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
                return UserService.profile()
            },
            myEvents: function(EventService) {
                return EventService.myEvents();
            }
        }
    })
    .state('casting.home', {
        url: '/home',
        parent: 'casting',
        templateUrl: 'static/js/app/views/casting/home.html',
        controller: 'HomeController'
    })
    .state('casting.links', {
        url:'/events/:eventId/links',
        parent: 'casting',
        templateUrl: 'static/js/app/views/casting/link-requests.html',
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
    .state('casting.schedules', {
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
    })
    .state('casting.forms', {
        url: '/organizations/:organizationId/forms',
        parent: 'casting',
        templateUrl: 'static/js/app/views/casting/rating-form.html',
        controller: 'RatingFormController',
        resolve: {
            fields: function($stateParams, RatingService) {
                return RatingService.formFields($stateParams.organizationId);
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