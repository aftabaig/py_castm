castM.controller("BroadcastController", ['$scope', '$rootScope', '$location', '$localStorage', 'BroadcastService', 'talentAttendees', 'castingAttendees', function($scope, $rootScope, $location, $localStorage, BroadcastService, talentAttendees, castingAttendees) {

    $scope.event = event;
    $scope.talentAttendees = talentAttendees;
    $scope.castingAttendees = castingAttendees;

    $scope.recipients = [
        "All Casting",
        "All Talents",
        "All Users"
    ];

    $scope.send = function() {



    }


}]);