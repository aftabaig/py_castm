lc.controller("EntitiesController", ['$scope', '$rootScope', '$localStorage', 'EntityService', 'EntityHelper', 'entities', function($scope, $rootScope, $localStorage, EntityService, EntityHelper, entities) {

    $rootScope.activeMenu = "Entities";
    $rootScope.currentUser = $localStorage.user;

    $scope.entities = entities;

    $scope.deleteEntity = function(index) {
        var entity = $scope.entities[index];
        if (entity)
        {
            $scope.promise = EntityService.delete(entity.id)
            .then(function() {
                $scope.entities.splice(index, 1);
            })
        }
    }

    $scope.formatAddress = function(entity) {
        return EntityHelper.formattedAddress(entity);
    }

}]);