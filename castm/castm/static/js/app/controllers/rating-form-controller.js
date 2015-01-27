castM.controller("RatingFormController", ['$scope', '$rootScope', '$location', '$localStorage', 'RatingService', 'fields', function($scope, $rootScope, $location, $localStorage, RatingService, fields) {

    $scope.fields = fields;
    $scope.fieldTypes = RatingService.fieldTypes();
    $scope.newField = {}

    // Clears the new field.
    // Called after a new field is added.
    $scope.clearField = function() {
        $scope.newField = {}
    }

    // Sends add field request to server.
    $scope.addNewField = function() {

        var field = $scope.newField;

        // In case of a "Radio Button", manually fill-up
        // the items array with option1 and option2.
        if (field.type === 'RDB') {
            var option1 = {
                "title": $scope.newField.option1,
                "value": $scope.newField.option1
            }
            var option2 = {
                "title": $scope.newField.option2,
                "value": $scope.newField.option2
            }
            field.items = [
                option1,
                option2
            ]
        }
        // In case of a "Text Field" or "Multi-line Text Field",
        // the items array should be empty.
        else if (field.type === 'TXT' || field.type === 'MUL' || field.type === 'SCL') {
            field.items = []
        }

        // Finally, send add field request to server.
        RatingService.addField($scope.profile.organization.organization_id, field)
        .then(function(addedField) {
            $scope.newField = {}
            field.id = addedField.id;
            $scope.fields.push(field)
        }, function(error) {
            alert(error.message);
        });

    }

    $scope.updateField = function(index) {

        var field = $scope.fields[index];
        if (field) {

            if (field.type === 'RDB') {
                var option1 = {
                    "title": $scope.newField.option1,
                    "value": $scope.newField.option1
                }
                var option2 = {
                    "title": $scope.newField.option2,
                    "value": $scope.newField.option2
                }

                if (!field.deleted_items) {
                    field.deleted_items = []
                }
                field.items.forEach(function(item) {
                    field.deleted_items.push(item);
                });

                field.items = [
                    option1,
                    option2
                ]
            }
            // In case of a "Text Field" or "Multi-line Text Field",
            // the items array should be empty.
            else if (field.type === 'TXT' || field.type === 'MUL' || field.type === 'SCL') {

                if (!field.deleted_items) {
                    field.deleted_items = []
                }
                field.items.forEach(function(item) {
                    field.deleted_items.push(item);
                });

                field.items = []
            }

            // Finally, send update field request to server.
            RatingService.updateField($scope.profile.organization.organization_id, field)
            .then(function(addedField) {
                $scope.newField = {}
                field.id = addedField.id;
                $scope.fields.push(field)
            }, function(error) {
                alert(error.message);
            });

        }

    }

    // Sends delete field request to server.
    $scope.deleteField = function(index) {

        var field = $scope.fields[index];
        if (field) {
            RatingService.deleteField($scope.profile.organization.organization_id, field.id)
            .then(function(message) {
                setTimeout(function() {
                    $scope.$apply(function() {
                       $scope.fields.splice(index, 1);
                    })
                }, 100)
            }, function(error) {
                alert(error.message);
            })
        }

    }

    $scope.addItem = function(index) {

        field = $scope.newField;
        if (index > 0) {
            field = $scope.fields[index];
        }

        if (field) {
            if (!field.items) {
                field.items = [];
            }
            field.items.push({
                "title": $scope.newItem,
                "value": $scope.newItem
            })
            $scope.newItem = "";
        }

    }

    $scope.removeItem = function(index, itemIndex) {

        field = $scope.newField;
        if (index > 0) {
            field = $scope.fields[index];
        }

        if (field) {
            if (!field.deleted_items) {
                field.deleted_items = [];
            }
            field.deleted_items.push(field.items[itemIndex]);
            field.items.splice(itemIndex, 1);
        }
    }

    $scope.toggleUseStars = function(index) {

        field = $scope.newField;
        if (index > 0) {
            field = $scope.fields[index];
        }

        if (field) {
            field.use_stars = !field.use_stars;
        }

    }

}]);