castM.controller("RatingFormController", ['$scope', '$rootScope', '$location', '$localStorage', 'RatingService', 'fields', function($scope, $rootScope, $location, $localStorage, RatingService, fields) {

    $scope.fields = fields;
    $scope.fieldTypes = RatingService.fieldTypes();
    $scope.newField = {}
    $scope.updating = false;
    $scope.error = "";

    // Clears the new field.
    // Called after a new field is added.
    $scope.clearField = function() {
        $scope.newField = {}
    }

    $scope.validate = function(field) {

        if (!field.title || field.title.length == 0) {
            field.message = "Title cannot be empty";
            return false;
        }
        if (!field.type || field.type.length == 0) {
            field.message = "Select type of field";
            return false;
        }
        if (field.type === 'RAD') {
            if (!field.option1 || field.option1.length == 0 ||
                !field.option2 || field.option2.length == 0) {
                field.message = "Both option1 and option2 are required"
                return false;
            }
        }
        if (field.type === 'DRPD' || field.type === 'CHK') {
            if (!field.items || field.items.length < 2) {
                field.message = "A drop-down/check-box needs to have at-lease 2 or more items"
                return false;
            }
        }

        field.message = "";
        return true;

    }

    // Sends add field request to server.
    $scope.addNewField = function() {

        var field = $scope.newField;

        if (!$scope.validate(field)) {
            return;
        }

        // In case of a "Radio Button", manually fill-up
        // the items array with option1 and option2.
        if (field.type === 'RAD') {
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

        $scope.updating = true;

        // Finally, send add field request to server.
        RatingService.addField($scope.profile.organization.organization_id, field)
        .then(function(addedField) {
            $scope.newField = {}
            field.id = addedField.id;
            $scope.fields.push(field);
            $scope.updating = false;
        }, function(error) {
            $scope.updating = false;
            field.message = error.message;
        });

    }

    $scope.updateField = function(index) {

        var field = $scope.fields[index];

        if (!$scope.validate(field)) {
            return;
        }

        if (field) {

            if (field.updating) {
                return;
            }

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

            field.updating = true;

            // Finally, send update field request to server.
            RatingService.updateField($scope.profile.organization.organization_id, field)
            .then(function(updatedField) {
                field.updating = false;
            }, function(error) {
                field.updating = false;
                field.error = error.message;
            });

        }

    }

    $scope.confirmDelete = function(index) {

        var field = $scope.fields[index];
        if (field) {
            if (field.updating) {
                return;
            }
            field.showDeleteConfirmation = true;
        }
    }

    // Sends delete field request to server.
    $scope.deleteField = function(index) {

        var field = $scope.fields[index];
        if (field) {

            field.showDeleteConfirmation = false;
            field.updating = true;

            RatingService.deleteField($scope.profile.organization.organization_id, field.id)
            .then(function(message) {
                setTimeout(function() {
                    $scope.$apply(function() {
                       $scope.fields.splice(index, 1);
                       field.updating = false;
                    })
                }, 100)
            }, function(error) {
                field.message = error.message;
                field.updating = false;
            })
        }

    }

    $scope.addItem = function(index) {

        field = $scope.newField;
        if (index > 0) {
            field = $scope.fields[index];
        }
        console.log($scope.newItem);
        if (field) {
            if (!field.items) {
                field.items = [];
            }
            field.items.push({
                "title": $scope.newItem,
                "value": $scope.newItem
            });
            console.log(index);
            console.dir(field);
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