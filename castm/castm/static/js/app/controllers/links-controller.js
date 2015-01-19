castM.controller("LinksController", ['$scope', '$rootScope', '$location', '$localStorage', 'EventService', 'event', 'qualifiedTalentAttendees', 'qualifiedCastingAttendees', 'pendingTalentAttendees', 'pendingCastingAttendees', function($scope, $rootScope, $location, $localStorage, EventService, event, qualifiedTalentAttendees, qualifiedCastingAttendees, pendingTalentAttendees, pendingCastingAttendees) {

    $scope.event = event;
    $scope.talentAttendees = talentAttendees;
    $scope.castingAttendees = castingAttendees;

    $scope.acceptRequest = function(index, isTalent) {

        // Get reference to attendee.
        var attendee;
        if (isTalent) {
            attendee = $scope.talentAttendees[index];
        }
        else {
            attendee = $scope.castingAttendees[index];
        }

        // Send "accept" request to server.
        EventService.acceptRequest(event.event_id, attendee.id)
        .then(function(data) {
            setTimeout(function() {
                $scope.$apply(function() {
                    attendee.is_accepted = true;
                    attendee.is_rejected = false;
                });
            }, 100);
        }, function(error) {

        });

    }

    $scope.rejectRequest = function(requestId, isTalent) {

        // Get reference to attendee.
        var attendee;
        if (isTalent) {
            attendee = $scope.talentAttendees[index];
        }
        else {
            attendee = $scope.castingAttendees[index];
        }

        // Send "reject" request to server.
        EventService.rejectRequest(event.event_id, attendee.id)
        .then(function(data) {
            setTimeout(function() {
                $scope.$apply(function() {
                    attendee.is_accepted = false;
                    attendee.is_rejected = true;
                });
            }, 100);
        }, function(error) {

        });

    }

}]);