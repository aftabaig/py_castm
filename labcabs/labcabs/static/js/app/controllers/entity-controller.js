lc.controller("EntityController", ['$scope', '$rootScope', '$location', '$localStorage', 'EntityService', 'entity', function($scope, $rootScope, $location, $localStorage, EntityService, entity) {

  $rootScope.activeMenu = "Entities";
  $rootScope.currentUser = $localStorage.user;

  $scope.entity = entity;
  if ($scope.entity) {
    $scope.isNew = false;
  }
  else {
    $scope.entity = {}
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

  $scope.addAccount = function() {
    if (!$scope.entity.accounts) {
        $scope.entity.accounts = [];
    }
    $scope.entity.accounts.push({
        "description": "",
        "isNew": true
    });
  }

  $scope.doneAddAccount = function(index) {
    $scope.entity.accounts[index].isNew = false;
  }

  $scope.cancelAddAccount = function(index) {
    $scope.entity.accounts.splice(index, 1);
  }

  $scope.removeAccount = function(index) {
    $scope.entity.accounts.splice(index, 1);
  }

}]);

