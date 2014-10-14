lc.controller("ConsignmentsController", ['$scope', '$rootScope', '$localStorage', 'ConsignmentService', 'consignments', function($scope, $rootScope, $localStorage, ConsignmentService, consignments) {

    $rootScope.activeMenu = "Consignments";
    $rootScope.currentUser = $localStorage.user;

    $scope.consignments = consignments;
    console.log("consignments:");
    console.dir($scope.consignments);
    $scope.delete = function(index) {
        var consignment = $scope.consignments[index];
        if (consignment)
        {
            ConsignmentService.delete(consignment.id)
            .then(function() {
                $scope.consignments.splice(index, 1);
            })
        }
    }

}]);