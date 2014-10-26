lc.directive('multiEntitySelector', function () {
    return {
        restrict: 'E',
        scope: {
            entities: '=',
            exportAction: '&'
        },
        link: function($scope, element, attrs) {

            $scope.toggleEntity = function($event, index) {
                var entity = $scope.entities[index];
                entity.selectedForExport = !entity.selectedForExport;
                $event.stopImmediatePropagation();
            }

        },
        templateUrl: 'static/js/directives/multi-entity-selector.html'
    }
});