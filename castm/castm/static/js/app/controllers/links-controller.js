castM.controller("LinksController", ['$scope', '$rootScope', '$location', '$localStorage', 'EventService', 'event', 'qualifiedTalentAttendees', 'qualifiedCastingAttendees', 'pendingTalentAttendees', 'pendingCastingAttendees', function($scope, $rootScope, $location, $localStorage, EventService, event, qualifiedTalentAttendees, qualifiedCastingAttendees, pendingTalentAttendees, pendingCastingAttendees) {

    $scope.event = event;
    $scope.qualifiedTalentAttendees = qualifiedTalentAttendees;
    $scope.qualifiedCastingAttendees = qualifiedCastingAttendees;
    $scope.pendingTalentAttendees = pendingTalentAttendees;
    $scope.pendingCastingAttendees = pendingCastingAttendees;

    $scope.acceptRequest = function(requestId) {

    }

    $scope.rejectRequest = function(requestId) {

    }

}]);