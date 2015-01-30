castM.controller("LinksController", ['$scope', '$rootScope', '$location', '$localStorage', 'EventService', 'event', 'talentAttendees', 'castingAttendees', function($scope, $rootScope, $location, $localStorage, EventService, event, talentAttendees, castingAttendees) {

    $scope.event = event;
    $scope.talentAttendees = talentAttendees;
    $scope.castingAttendees = castingAttendees;

    $scope.acceptRequest = function(index, isTalent) {
console.log(index);
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
            setTimeout(function() {
                $scope.$apply(function() {
                    attendee.updating = false;
                    attendee.is_accepted = true;
                    attendee.is_rejected = false;
                });
            }, 100);
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
            setTimeout(function() {
                $scope.$apply(function() {
                    attendee.is_accepted = false;
                    attendee.is_rejected = true;
                });
            }, 100);
        }, function(error) {
            attendee.updating = false;
            attendee.message = error.message;
        });

    }

}]);