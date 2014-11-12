lc.controller("SuppliesController", ['$scope', '$rootScope', '$localStorage', 'SupplyService', 'supplies', function($scope, $rootScope, $localStorage, SupplyService, supplies) {

    $rootScope.activeMenu = "";
    $rootScope.currentUser = $localStorage.user;

    $scope.supplies = supplies;

    $scope.addSupply = function() {
        $scope.supplies.push({
            "description": "",
            "isNew": true,
            "isEditing": true
        });
    }

    $scope.cancelAdd = function(index) {
        $scope.supplies.splice(index, 1);
    }

    $scope.saveSupply = function(index) {
        $scope.promise = SupplyService.add($scope.supplies[index])
        .then(function() {
            $scope.supplies[index].isNew = false;
            $scope.supplies[index].isEditing = false;
        });
    }

    $scope.editSupply = function(index) {
        $scope.supplies[index].isEditing = true;
    }

    $scope.cancelEdit = function(index) {
        $scope.supplies[index].isEditing = false;
    }

    $scope.updateSupply = function(index) {
        $scope.promise = SupplyService.update($scope.supplies[index])
        .then(function() {
            $scope.supplies[index].isEditing = false;
        });
    }

    $scope.deleteSupply = function(index) {
        var supply = $scope.supplies[index];
        if (supply)
        {
            $scope.promise = SupplyService.delete(supply.id)
            .then(function() {
                $scope.supplies.splice(index, 1);
            })
        }
    }


}]);