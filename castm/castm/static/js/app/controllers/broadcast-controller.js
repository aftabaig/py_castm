castM.controller("BroadcastController", ['$scope', '$rootScope', '$location', '$localStorage', 'BroadcastService', 'event', 'talentAttendees', 'castingAttendees', function($scope, $rootScope, $location, $localStorage, BroadcastService, event, talentAttendees, castingAttendees) {

    $scope.event = event;
    $scope.talentAttendees = talentAttendees;
    $scope.castingAttendees = castingAttendees;

    $scope.send = function() {

        $scope.errorMessage = "";
        $scope.info = "";
        $scope.working = true;

        if (!$scope.to) {
            $scope.errorMessage = "Please select recipients";
            return;
        }
        if (!$scope.message) {
            $scope.errorMessage = "Please enter a message";
            return;
        }

        BroadcastService.broadcast($scope.event.event_id, $scope.to, $scope.message)
        .then(function(data) {
            $scope.working = false;
            $scope.message = "";
            $scope.to = "";
            $scope.info = "Message sent";
        }, function(error) {
            $scope.working = false;
            $scope.errorMessage = error.message;
        })

    }


}]);