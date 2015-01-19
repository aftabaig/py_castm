castM.controller("ScheduleController", ['$scope', '$rootScope', '$location', '$localStorage', 'ScheduleService', 'event', 'schedules', 'talentAttendees', function($scope, $rootScope, $location, $localStorage, ScheduleService, event, schedules, talentAttendees) {

    $scope.event = event;
    $scope.schedules = schedules;
    $scope.talentAttendees = talentAttendees;

}]);