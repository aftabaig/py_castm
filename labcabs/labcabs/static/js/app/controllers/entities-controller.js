lc.controller("EntitiesController", ['$scope', '$rootScope', '$localStorage', 'EntityService', 'EntityHelper', 'entities', 'entityTypes', function($scope, $rootScope, $localStorage, EntityService, EntityHelper, entities, entityTypes) {

    $rootScope.activeMenu = "Entities";
    $rootScope.currentUser = $localStorage.user;

    $scope.entities = entities;
    $scope.entityTypes = entityTypes;
    $scope.filteredEntities = angular.copy(entities);

    $scope.filter = function() {
        if ($scope.selectedType) {
            $scope.filteredEntities = [];
            $scope.entities.forEach(function(entity) {
                if (entity.type === $scope.selectedType.type) {
                    $scope.filteredEntities.push(entity);
                }
            });
        }
        else {
            $scope.filteredEntities = angular.copy($scope.entities);
        }
    }

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