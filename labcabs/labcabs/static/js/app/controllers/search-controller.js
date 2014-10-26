lc.controller("SearchController", ['$scope', '$rootScope', '$location', '$localStorage', 'SearchService', 'ConsignmentService', 'EntityHelper', 'mySearches', 'consignments', 'entities', function($scope, $rootScope, $location, $localStorage, SearchService, ConsignmentService, EntityHelper, mySearches, consignments, entities) {

  $rootScope.activeMenu = "Search";
  $rootScope.currentUser = $localStorage.user;

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

  $scope.entities.forEach(function(entity) {
    entity.selectedForExport = true;
  })

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
  $scope.filteredConsignments.forEach(function(consignment) {
    consignment.exportable = true;
  });
  $scope.allConsignments = true;

  $scope.search = function() {

    $scope.filteredConsignments = angular.copy($scope.consignments);
    $scope.filteredConsignments.forEach(function(consignment) {
        consignment.exportable = true;
    });
    $scope.allConsignments = true;

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
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.pickup_postcode.match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for pickup state.
    if ($scope.pickupState) {

        var re = new RegExp($scope.pickupState, 'i');
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.pickup_state.match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for delivery postcode.
    if ($scope.deliveryPostcode) {

        var re = new RegExp($scope.deliveryPostcode, 'i');
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.delivery_postcode.match(re)) {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for delivery state.
    if ($scope.deliveryState) {

        var re = new RegExp($scope.deliveryState, 'i');
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            if (!consignment.delivery_state.match(re)) {
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
    if ($scope.pickupStartDate && $scope.pickupEndDate) {
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            var pickupDate = new Date(consignment.pickupDate);
            if (pickupDate >= $scope.pickupStartDate && pickupDate <= $scope.pickupEndDate) {
            }
            else {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

    // Search for eta date.
    if ($scope.etaStartDate && $scope.etaEndDate) {
        for (i=0; i<$scope.filteredConsignments.length; i++) {
            var consignment = $scope.filteredConsignments[i];
            var etaDate = new Date(consignment.eta_date);
            if (etaDate >= $scope.etaStartDate && etaDate <= $scope.etaEndDate) {
            }
            else {
                $scope.filteredConsignments.splice(i--, 1);
            }
        }
    }

  }

  $scope.yesterday = function() {
    var start = new moment().subtract("days", 1).startOf("day");
    var copy = angular.copy(start);
    var end = copy.add("hours", 23).add("minutes", 59).add("seconds", 59);
    return {
        "start": start.format("DD-MMM-YYYY HH:mm"),
        "end": end.format("DD-MMM-YYYY HH:mm")
    }
  }

  $scope.today = function() {
    var start = new moment().startOf("day");
    var copy = angular.copy(start);
    var end = copy.add("hours", 23).add("minutes", 59).add("seconds", 59);
    return {
        "start": start.format("DD-MMM-YYYY HH:mm"),
        "end": end.format("DD-MMM-YYYY HH:mm")
    }
  }

  $scope.tomorrow = function() {
    var start = new moment().add("days", 1).startOf("day");
    var copy = angular.copy(start);
    var end = copy.add("hours", 23).add("minutes", 59).add("seconds", 59);
    return {
        "start": start.format("DD-MMM-YYYY HH:mm"),
        "end": end.format("DD-MMM-YYYY HH:mm")
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
    if ($scope.pickupStartDate) {
        searchObj.criteria.push({
            "criterion": "pickup_start_date",
            "criterion_value": $scope.pickupStartDate
        });
    }
    if ($scope.pickupEndDate) {
        searchObj.criteria.push({
            "criterion": "pickup_end_date",
            "criterion_value": $scope.pickupEndDate
        });
    }
    if ($scope.etaStartDate) {
        searchObj.criteria.push({
            "criterion": "eta_start_date",
            "criterion_value": $scope.etaStartDate
        });
    }
    if ($scope.etaEndDate) {
        searchObj.criteria.push({
            "criterion": "eta_end_date",
            "criterion_value": $scope.etaEndDate
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
    $scope.pickupStartDate = "";
    $scope.pickupEndDate = "";
    $scope.etaStartDate = "";
    $scope.etaEndDate = "";

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
            else if (criterion.criterion === "pickup_start_date") {
                $scope.pickupStartDate = criterion.criterion_value;
            }
            else if (criterion.criterion === "pickup_end_date") {
                $scope.pickupEndDate = criterion.criterion_value;
            }
            else if (criterion.criterion === "eta_start_date") {
                $scope.etaStartDate = criterion.criterion_value;
            }
            else if (criterion.criterion === "eta_end_date") {
                $scope.etaEndDate = criterion.criterion_value;
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

  $scope.toggleConsignment = function(index, $event) {
    var consignment = $scope.filteredConsignments[index];
    var checkbox = $event.target;
    consignment.exportable = checkbox.checked;

    var totalSelected = 0;
    $scope.filteredConsignments.forEach(function(consignment) {
        if (consignment.exportable) {
            totalSelected++;
        }
    });

    $scope.allConsignments = (totalSelected == $scope.filteredConsignments.length);

  }

  $scope.toggleAllConsignments = function($event) {
    var checkbox = $event.target;
    $scope.filteredConsignments.forEach(function(consignment) {
        consignment.exportable = checkbox.checked;
    });
    $scope.allConsignments = checkbox.checked;

  }

  $scope.allConsignmentsSelected = function() {
    $scope.filteredConsignments.forEach(function(consignment) {
        if (!consignment.exportable) {
            return false;
        }
    });
    return true;
  }

  $scope.export = function() {

    var exportIds = [];
    $scope.filteredConsignments.forEach(function(consignment) {
        if (consignment.exportable) {
            exportIds.push(consignment.id);
        }
    });

    var subject;
    if ($scope.selectedSearch.name) {
        subject = "Your Consignments - " + $scope.selectedSearch.name;
    }
    else {
        subject = "Your Consignments";
    }

    var exportableEntities = [];
    $scope.entities.forEach(function(entity) {
        if (entity.selectedForExport) {
            exportableEntities.push(entity);
        }
    });

    ConsignmentService.send(subject, exportIds, exportableEntities, $scope.fields)
    .then(function(data) {
        console.log("email sent");
    });
  }

  $scope.openPickupStart = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.openedPickupStart = true;
    $scope.openedPickupEnd = false;
    $scope.openedETAStart = false;
    $scope.openedETAEnd = false;
  };

  $scope.openPickupEnd = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.openedPickupStart = false;
    $scope.openedPickupEnd = true;
    $scope.openedETAStart = false;
    $scope.openedETAEnd = false;
  };

  $scope.openETAStart = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.openedPickupStart = false;
    $scope.openedPickupEnd = false;
    $scope.openedETAStart = true;
    $scope.openedETAEnd = false;
  };

  $scope.openETAEnd = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.openedPickupStart = false;
    $scope.openedPickupEnd = false;
    $scope.openedETAStart = false;
    $scope.openedETAEnd = true;
  };

  $scope.formatAddress = function(entity) {
    return EntityHelper.formattedAddress(entity);
  }

  $scope.formatPickupAddress = function(consignment) {

    var address = '';
    if (consignment.pickup_tenancy) {
        address = address + ' ' + consignment.pickup_tenancy;
    }
    if (consignment.pickup_street_num) {
        address = address + ' Street # ' + consignment.pickup_street_num;
    }
    if (consignment.pickup_street) {
        address = address + ' ' + consignment.pickup_street;
    }
    if (consignment.pickup_town) {
        address = address + ' ' + consignment.pickup_town;
    }
    if (consignment.pickup_postcode) {
        address = address + ' ' + consignment.pickup_postcode;
    }
    if (consignment.pickup_state) {
        address = address + ' ' + consignment.pickup_state;
    }
    if (consignment.pickup_country) {
        address = address + ' ' + consignment.pickup_country;
    }
    return address;

  }

  $scope.formatDeliveryAddress = function(consignment) {

    var address = '';
    if (consignment.delivery_tenancy) {
        address = address + ' ' + consignment.delivery_tenancy;
    }
    if (consignment.delivery_street_num) {
        address = address + ' Street # ' + consignment.delivery_street_num;
    }
    if (consignment.delivery_street) {
        address = address + ' ' + consignment.delivery_street;
    }
    if (consignment.delivery_town) {
        address = address + ' ' + consignment.delivery_town;
    }
    if (consignment.delivery_postcode) {
        address = address + ' ' + consignment.delivery_postcode;
    }
    if (consignment.delivery_state) {
        address = address + ' ' + consignment.delivery_state;
    }
    if (consignment.delivery_country) {
        address = address + ' ' + consignment.delivery_country;
    }
    return address;

  }

}]);