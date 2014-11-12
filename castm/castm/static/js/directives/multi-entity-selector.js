lc.directive('multiEntitySelector', function () {
    return {
        restrict: 'E',
        scope: {
            entities: '=',
            exportAction: '&'
        },
        link: function($scope, element, attrs) {

            $('[data-toggle="popover"]').popover({
                trigger: 'hover',
                'placement': 'top'
            });

            $scope.toggleEntity = function($event, index) {
                var entity = $scope.entities[index];
                entity.selectedForExport = !entity.selectedForExport;
                $event.stopImmediatePropagation();
            };

            $scope.filterFocus = function($event) {
                console.log("event");
                console.dir($event);
                $event.stopImmediatePropagation();
            }

        },
        templateUrl: 'static/js/directives/multi-entity-selector.html'
    }
});