lc.controller("SearchController", ['$scope', '$rootScope', '$location', '$localStorage', 'EntityHelper', 'consignments', 'entities', function($scope, $rootScope, $location, $localStorage, EntityHelper, consignments, entities) {

  $rootScope.activeMenu = "Search";
  $rootScope.currentUser = $localStorage.user;

  $scope.statuses = [
    'Quote',
    'Booked',
    'Transit',
    'Delivered',
    'Hold',
    'Templates'
  ];

  $scope.modes = [
    'Same Day',
    'Overnight',
    'Next Flight'
  ];

  $scope.promise = null;
  $scope.message = "";

  $scope.consignments = consignments;
  $scope.entities = entities;

  $scope.consignments.forEach(function(consignment) {
    $scope.entities.forEach(function(entity) {
        if (consignment.consignor == entity.id) {
            consignment.consignorObj = angular.copy(entity);
        }
        if (consignment.consignee == entity.id) {
            consignment.consigneeObj = angular.copy(entity);
        }
    });
  });

  console.log("all consignments");
  console.dir($scope.consignments);

  $scope.filteredConsignments = []

  $scope.search = function() {

    $scope.filteredConsignments = angular.copy($scope.consignments);

    if ($scope.consignor) {
        var re = new RegExp($scope.consignor, 'i');
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.consignor.toString().match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    if ($scope.consignee) {
        var re = new RegExp($scope.consignee, 'i');
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.consignee.toString().match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    if ($scope.postcode) {

        var re = new RegExp($scope.postcode, 'i');
        var filteredEntities = []
        for (i=0; i<$scope.entities.length; i++) {
            var entity = $scope.entities[i];
            if (entity.postcode.match(re)) {
                filteredEntities.push(entity.id);
            }
        }
        console.log("filtered-entities");
        console.dir(filteredEntities);

        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            var found = false;
            filteredEntities.forEach(function(entity) {
                console.log("consignee",consignment.consignee);
                if (consignment.consignee === entity) {
                    found = true;
                }
            });
            if (!found) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    if ($scope.state) {

        var re = new RegExp($scope.state, 'i');
        var filteredEntities = []
        for (i=0; i<$scope.entities.length; i++) {
            var entity = $scope.entities[i];
            if (entity.state.match(re)) {
                filteredEntities.push(entity.id);
            }
        }

        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            var found = false;
            filteredEntities.forEach(function(entity) {
                if (consignment.consignee == entity.id) {
                    found = true;
                }
            });
            if (!found) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    if ($scope.account) {
        var re = new RegExp($scope.account, 'i');
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.account.match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    if ($scope.mode) {
         var re = new RegExp($scope.mode, 'i');
         for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.mode.match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    if ($scope.status) {
         var re = new RegExp($scope.status, 'i');
         for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.status.match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    if ($scope.startDate && $scope.endDate) {
        console.log("yes");
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            var pickupDate = new Date(consignment.pickupDate);
            if (pickupDate >= $scope.startDate && pickupDate <= $scope.endDate) {
                console.log("ok");
            }
            else {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    console.dir($scope.filteredConsignments);

  }

  $scope.openStart = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.openedEnd = false;
    $scope.openedStart = true;
  };

  $scope.openEnd = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.openedStart = false;
    $scope.openedEnd = true;
  };

  $scope.formatAddress = function(entity) {
    return EntityHelper.formattedAddress(entity);
  }

}]);