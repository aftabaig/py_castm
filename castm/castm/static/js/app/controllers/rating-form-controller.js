castM.controller("RatingFormController", ['$scope', '$rootScope', '$location', '$localStorage', 'RatingService', 'fields', function($scope, $rootScope, $location, $localStorage, RatingService, fields) {

    $scope.fields = fields;
    $scope.fieldTypes = RatingService.fieldTypes();
    $scope.newField = {}

    $scope.addField = function() {

        var field = {}
        field.title = $scope.newField.title;
        field.type = $scope.newField.type;
        field.items = [
            $scope.newField.option1,
            $scope.newField.option2
        ]
        RatingService.addField($scope.profile.organization.organization_id, field)
        .then(function(field) {

        }, function(error) {

        });

    }

}]);