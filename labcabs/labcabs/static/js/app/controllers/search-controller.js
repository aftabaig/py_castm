lc.controller("SearchController", ['$scope', '$rootScope', '$location', '$localStorage', 'SearchService', 'ConsignmentService', 'EntityHelper', 'mySearches', 'consignments', 'entities', function($scope, $rootScope, $location, $localStorage, SearchService, ConsignmentService, EntityHelper, mySearches, consignments, entities) {

  $rootScope.activeMenu = "Search";
  $rootScope.currentUser = $localStorage.user;

  $scope.exportableConsignmentId = 8;

  $scope.saveMode = false;
  $scope.setSaveMode = function(mode) {
    $scope.saveMode = mode;
  }

  $scope.statuses = [
    'Quote',
    'Booked',
    'Transit',
    'Delivered',
    'Hold',
    'Templates'
  ];

  $scope.modes = [
    'Same Day Air',
    'Overnight Air',
    'Perishable Air',
    'Road Express',
    'Off Peak Air'
  ];

  $scope.fields = [];
  $scope.fields.push({
    'name': 'consignor',
    'title': 'Consignor',
    'selected': true
  });
  $scope.fields.push({
    'name': 'consignee',
    'title': 'Consignee',
    'selected': true
  });
  $scope.fields.push({
    'name': 'originator',
    'title': 'Originator',
    'selected': true
  });
  $scope.fields.push({
    'name': 'account',
    'title': 'Account',
    'selected': true
  });
  $scope.fields.push({
    'name': 'pickup_address',
    'title': 'Pickup Address',
    'selected': true
  });
  $scope.fields.push({
    'name': 'delivery_address',
    'title': 'Delivery Address',
    'selected': true
  });
  $scope.fields.push({
    'name': 'mode',
    'title': 'Mode',
    'selected': true
  });
  $scope.fields.push({
    'name': 'status',
    'title': 'Status',
    'selected': true
  });
  $scope.fields.push({
    'name': 'pickup_date',
    'title': 'Pickup Date',
    'selected': true
  });
  $scope.fields.push({
    'name': 'eta_date',
    'title': 'ETA Date',
    'selected': true
  });
  $scope.fields.push({
    'name': 'notes',
    'title': 'Notes',
    'selected': true
  });
  $scope.fields.push({
    'name': 'customer_reference',
    'title': 'Customer Reference',
    'selected': true
  });

  $scope.promise = null;
  $scope.message = "";

  $scope.mySearches = mySearches;
  $scope.consignments = consignments;
  $scope.entities = entities;
  $scope.selectedSearch = {}

  $scope.consignments.forEach(function(consignment) {
    $scope.entities.forEach(function(entity) {
        if (consignment.consignor == entity.id) {
            consignment.consignorObj = angular.copy(entity);
        }
        if (consignment.consignee == entity.id) {
            consignment.consigneeObj = angular.copy(entity);
        }
        if (consignment.originator == entity.id) {
            consignment.originatorObj = angular.copy(entity);
            entity.accounts.forEach(function(account) {
                if (consignment.account == account.id) {
                    consignment.accountObj = angular.copy(account);
                }
            });
        }
    });
  });

  $scope.filteredConsignments = angular.copy($scope.consignments);

  $scope.search = function() {

    $scope.filteredConsignments = angular.copy($scope.consignments);

    // Search for consignor.
    if ($scope.consignor) {
        var re = new RegExp($scope.consignor, 'i');
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.consignor.toString().match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for consignee.
    if ($scope.consignee) {
        var re = new RegExp($scope.consignee, 'i');
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.consignee.toString().match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for pickup postcode.
    if ($scope.pickupPostcode) {

        var re = new RegExp($scope.pickupPostcode, 'i');
        var filteredEntities = []
        for (i=0; i<$scope.entities.length; i++) {
            var entity = $scope.entities[i];
            if (entity.postcode.match(re)) {
                filteredEntities.push(entity.id);
            }
        }

        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            var found = false;
            filteredEntities.forEach(function(entity) {
                if (consignment.consignor === entity) {
                    found = true;
                }
            });
            if (!found) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for pickup state.
    if ($scope.pickupState) {

        var re = new RegExp($scope.pickupState, 'i');
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
                if (consignment.consignor == entity) {
                    found = true;
                }
            });
            if (!found) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for delivery postcode.
    if ($scope.deliveryPostcode) {

        var re = new RegExp($scope.deliveryPostcode, 'i');
        var filteredEntities = []
        for (i=0; i<$scope.entities.length; i++) {
            var entity = $scope.entities[i];
            if (entity.postcode.match(re)) {
                filteredEntities.push(entity.id);
            }
        }

        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            var found = false;
            filteredEntities.forEach(function(entity) {
                if (consignment.consignee === entity) {
                    found = true;
                }
            });
            if (!found) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for delivery state.
    if ($scope.deliveryState) {

        var re = new RegExp($scope.deliveryState, 'i');
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
                if (consignment.consignee == entity) {
                    found = true;
                }
            });
            if (!found) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for account.
    if ($scope.account) {
        var re = new RegExp($scope.account, 'i');
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.account.match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for customer reference.
    if ($scope.customerReference) {
        console.log("customerReference:", $scope.customerReference);
        var re = new RegExp($scope.customerReference, 'i');
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.customer_reference.match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for mode.
    if ($scope.mode) {
         var re = new RegExp($scope.mode, 'i');
         for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.mode.match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for status.
    if ($scope.status) {
         var re = new RegExp($scope.status, 'i');
         for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.status.match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for pickup date.
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

  }

  // Save search.
  $scope.save = function() {

    // Create a new search object.
    var searchObj = {}
    searchObj.name = $scope.searchName;
    searchObj.fields = $scope.fields;

    searchObj.criteria = [];
    if ($scope.consignor) {
        searchObj.criteria.push({
            "criterion": "consignor",
            "criterion_value": $scope.consignor
        });
    }
    if ($scope.consignee) {
        searchObj.criteria.push({
            "criterion": "consignee",
            "criterion_value": $scope.consignee
        });
    }
    if ($scope.pickupPostcode) {
        searchObj.criteria.push({
            "criterion": "pickup_postcode",
            "criterion_value": $scope.pickupPostcode
        });
    }
    if ($scope.pickupState) {
        searchObj.criteria.push({
            "criterion": "pickup_state",
            "criterion_value": $scope.pickupState
        });
    }
    if ($scope.deliveryPostcode) {
        searchObj.criteria.push({
            "criterion": "delivery_postcode",
            "criterion_value": $scope.deliveryPostcode
        });
    }
    if ($scope.deliveryState) {
        searchObj.criteria.push({
            "criterion": "delivery_state",
            "criterion_value": $scope.deliveryState
        });
    }
    if ($scope.account) {
        searchObj.criteria.push({
            "criterion": "account",
            "criterion_value": $scope.account
        });
    }
    if ($scope.customerReference) {
        searchObj.criteria.push({
            "criterion": "customer_reference",
            "criterion_value": $scope.customerReference
        });
    }
    if ($scope.mode) {
        searchObj.criteria.push({
            "criterion": "mode",
            "criterion_value": $scope.mode
        });
    }
    if ($scope.status) {
        searchObj.criteria.push({
            "criterion": "status",
            "criterion_value": $scope.status
        });
    }
    if ($scope.startDate) {
        searchObj.criteria.push({
            "criterion": "start_date",
            "criterion_value": $scope.startDate
        });
    }
    if ($scope.endDate) {
        searchObj.criteria.push({
            "criterion": "end_date",
            "criterion_value": $scope.endDate
        });
    }
    console.log("searchObj");
    console.dir(searchObj);
    SearchService.add(searchObj)
    .then(function(data) {
        $scope.mySearches.unshift(searchObj);
        $scope.setSaveMode(false);
    });

  }

  $scope.loadSearch = function() {

    var mySearch = $scope.selectedSearch;

    $scope.consignor = "";
    $scope.consignee = "";
    $scope.pickupPostcode = "";
    $scope.pickupState = "";
    $scope.deliveryPostcode = "";
    $scope.deliveryState= "";
    $scope.account = "";
    $scope.customerReference = "";
    $scope.mode = "";
    $scope.status = "";
    $scope.startDate = "";
    $scope.endDate = "";

    if (mySearch) {
        mySearch.criteria.forEach(function(criterion) {
            if (criterion.criterion === "consignor") {
                $scope.consignor = criterion.criterion_value;
            }
            else if (criterion.criterion === "consignee") {
                $scope.consignee = criterion.criterion_value;
            }
            else if (criterion.criterion === "pickup_postcode") {
                $scope.pickupPostcode = criterion.criterion_value;
            }
            else if (criterion.criterion === "pickup_state") {
                $scope.pickupState = criterion.criterion_value;
            }
            else if (criterion.criterion === "delivery_postcode") {
                $scope.deliveryPostcode = criterion.criterion_value;
            }
            else if (criterion.criterion === "delivery_state") {
                $scope.deliveryState = criterion.criterion_value;
            }
            else if (criterion.criterion === "account") {
                $scope.account = criterion.criterion_value;
            }
            else if (criterion.criterion === "customer_reference") {
                $scope.customerReference = criterion.criterion_value;
            }
            else if (criterion.criterion === "mode") {
                $scope.mode = criterion.criterion_value;
            }
            else if (criterion.criterion === "status") {
                $scope.status = criterion.criterion_value;
            }
            else if (criterion.criterion === "start_date") {
                $scope.startDate = criterion.criterion_value;
            }
            else if (criterion.criterion === "end_date") {
                $scope.endDate = criterion.criterion_value;
            }
         });
         $scope.fields = mySearch.fields;
    }
    else {
        $scope.selectAllFields();
    }
    $scope.search();
  }

  $scope.removeSelectedSearch = function() {

    SearchService.delete($scope.selectedSearch.id)
    .then(function(data) {
        var index = $scope.mySearches.indexOf($scope.selectedSearch);
        $scope.mySearches.splice(index, 1);
    });

  }

  $scope.selectAllFields = function() {
    $scope.fields.forEach(function(field) {
        field.selected = true;
    });
  }

  $scope.isFieldSelected = function(fieldName) {
    var selected = false;
    $scope.fields.forEach(function(field) {
        if (field.name === fieldName) {
            selected = field.selected;
        }
    });
    return selected;
  }

  $scope.markAsExport = function(index) {
    $scope.exportableConsignmentId = $scope.filteredConsignments[index].id;
  }

  $scope.export = function() {
    console.dir($scope);
    alert($scope.exportableConsignmentId);
    ConsignmentService.email($scope.exportableConsignmentId, $scope.exportTo)
    .then(function(data) {
        console.log("email sent");
    });
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