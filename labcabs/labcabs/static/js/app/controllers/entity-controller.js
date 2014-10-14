lc.controller("EntityController", ['$scope', '$rootScope', '$location', '$localStorage', 'EntityService', 'entity', function($scope, $rootScope, $location, $localStorage, EntityService, entity) {

  $rootScope.activeMenu = "Entities";
  $rootScope.currentUser = $localStorage.user;

  $scope.promise = null;
  $scope.message = "";

  $scope.alert = {
    "show": false,
    "title": "",
    "message": ""
  }

  $scope.entity = entity;
  if ($scope.entity) {
    $scope.isNew = false;
  }
  else {
    $scope.isNew = true;
  }

  $scope.save = function() {
    console.dir($scope.entity);
    if ($scope.isNew) {
        $scope.message = "Adding ...";
        $scope.promise = EntityService.add($scope.entity)
        .then(function(data) {
            $location.path('#/entities/').replace;
        });
    }
    else {
        $scope.message = "Updating ...";
        $scope.promise = EntityService.update($scope.entity)
        .then(function(data) {
            $location.path('#/entities/').replace;
        });
    }
  }

  $scope.confirmDelete = function(index) {
    $scope.selectedIndex = index;
    $scope.alert.title = "Delete " + $scope.leases[index].name;
    $scope.alert.message = "Are you sure to delete this lease?";
    $scope.alert.show = true;

  }

  $scope.hideAlert = function() {
    $scope.alert.show = false;
  }

}]);

