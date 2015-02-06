castM.controller("LinksController", ['$scope', '$rootScope', '$location', '$localStorage', 'EventService', 'event', 'talentAttendees', 'castingAttendees', function($scope, $rootScope, $location, $localStorage, EventService, event, talentAttendees, castingAttendees) {

    $scope.event = event;
    $scope.talentAttendees = talentAttendees;
    $scope.castingAttendees = castingAttendees;

    $scope.currentTalentPage = 0;
    $scope.talentPageSize = 25;
    $scope.talentPageCount = function() {
        return Math.ceil($scope.talentAttendees.length/$scope.talentPageSize);
    }

    $scope.currentCastingPage = 0;
    $scope.castingPageSize = 25;
    $scope.castingPageCount = function() {
        return Math.ceil($scope.castingAttendees.length/$scope.castingPageSize);
    }

    $scope.acceptRequest = function(index, isTalent) {

        // Get reference to attendee.
        var attendee;
        if (isTalent) {
            attendee = $scope.talentAttendees[index];
        }
        else {
            attendee = $scope.castingAttendees[index];
        }

        attendee.updating = true;

        // Send "accept" request to server.
        EventService.acceptRequest(event.event_id, attendee.attendance_id)
        .then(function(data) {
            attendee.updating = false;
            attendee.is_accepted = true;
            attendee.is_rejected = false;
        }, function(error) {
            attendee.updating = false;
            attendee.message = error.message;
        });

    }

    $scope.rejectRequest = function(index, isTalent) {

        // Get reference to attendee.
        var attendee;
        if (isTalent) {
            attendee = $scope.talentAttendees[index];
        }
        else {
            attendee = $scope.castingAttendees[index];
        }

        attendee.updating = true;

        // Send "reject" request to server.
        EventService.rejectRequest(event.event_id, attendee.attendance_id)
        .then(function(data) {
            attendee.updating = false;
            attendee.is_accepted = false;
            attendee.is_rejected = true;
        }, function(error) {
            attendee.updating = false;
            attendee.message = error.message;
        });

    }

}]);