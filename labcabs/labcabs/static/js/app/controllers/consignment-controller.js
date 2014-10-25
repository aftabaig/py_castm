lc.controller("ConsignmentController", ['$scope', '$rootScope', '$location', '$localStorage', 'ConsignmentService', 'EntityHelper', 'consignment', 'entities', 'supplies', function($scope, $rootScope, $location, $localStorage, ConsignmentService, EntityHelper, consignment, entities, supplies) {

  $rootScope.activeMenu = "Consignments";
  $rootScope.currentUser = $localStorage.user;

  $scope.onConsignorChange = function(entityId) {
    $scope.entities.forEach(function(entity) {
        if (entity.id == entityId) {
            $scope.selectedConsignor = entity;
            $scope.consignment.pickup_tenancy = entity.tenancy;
            $scope.consignment.pickup_street_num = entity.street_num;
            $scope.consignment.pickup_street = entity.street;
            $scope.consignment.pickup_town = entity.town;
            $scope.consignment.pickup_postcode = entity.postcode;
            $scope.consignment.pickup_state = entity.state;
            $scope.consignment.pickup_country = entity.country;
        }
    });
  }

  $scope.onConsigneeChange = function(entityId) {
    $scope.entities.forEach(function(entity) {
        if (entity.id == entityId) {
            $scope.selectedConsignee = entity;
            $scope.consignment.delivery_tenancy = entity.tenancy;
            $scope.consignment.delivery_street_num = entity.street_num;
            $scope.consignment.delivery_street = entity.street;
            $scope.consignment.delivery_town = entity.town;
            $scope.consignment.delivery_postcode = entity.postcode;
            $scope.consignment.delivery_state = entity.state;
            $scope.consignment.delivery_country = entity.country;
        }
    });
  }

  $scope.onOriginatorChange = function(entityId, isFirstCall) {
    setTimeout(function() {
        $scope.$apply(function() {
            $scope.entities.forEach(function(entity) {
                if (entity.id == entityId) {
                    $scope.selectedOriginator = entity;
                    $scope.selectedAccounts = entity.accounts;
                    if (!isFirstCall) {
                        $scope.consignment.account = "";
                    }
                }
            });
        });
    }, 10);
  }

  $scope.consignment = consignment;
  $scope.entities = entities;
  $scope.supplies = supplies;

  if ($scope.consignment) {
    $scope.isNew = false;
    $scope.onOriginatorChange($scope.consignment.originator, true);
  }
  else {
    $scope.consignment = {}
    $scope.isNew = true;
  }

  // Consignment Entities.
  $scope.selectedConsignor = {}
  $scope.selectedConsignee = {}
  $scope.selectedOriginator = {}
  $scope.selectedAccounts = []

  $scope.environments = [
    'Ambient',
    'Refrigerated',
    'Frozen',
    'Cryo'
  ];

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

  $scope.save = function() {
    if ($scope.isNew) {
        $scope.message = "Adding ...";
        console.log("consignment-dates:");
        console.dir($scope.consignment);
        $scope.promise = ConsignmentService.add($scope.consignment)
        .then(function(data) {
            $location.path('consignments/').replace;
        });
    }
    else {
        $scope.message = "Updating ...";
        $scope.promise = ConsignmentService.update($scope.consignment)
        .then(function(data) {
            $location.path('consignments/').replace;
        });
    }
  }

  $scope.addItem = function() {
    if (!$scope.consignment.items) {
        $scope.consignment.items = [];
    }
    $scope.consignment.items.push({
        "width": "0",
        "length": "0",
        "height": "0",
        "dead_weight": "0.0",
        "temp": "",
        "isNew": true
    });
  }

  $scope.addSupply= function() {
    if (!$scope.consignment.supplies) {
        $scope.consignment.supplies = [];
    }
    $scope.consignment.supplies.push({
        "supply": "",
        "amount": "",
        "isNew": true
    });
  }

  $scope.addCharge = function() {
    if (!$scope.consignment.charges) {
        $scope.consignment.charges = [];
    }
    $scope.consignment.charges.push({
        "description": "",
        "quantity": "0",
        "cost": "0.00",
        "isNew": true
    });
  }

  $scope.doneAddItem = function(index) {
    $scope.consignment.items[index].isNew = false;
  }

  $scope.doneAddSupply = function(index) {
    $scope.consignment.supplies[index].isNew = false;
  }

  $scope.doneAddCharge = function(index) {
    $scope.consignment.charges[index].isNew = false;
  }

  $scope.cancelAddItem = function(index) {
    $scope.consignment.items.splice(index, 1);
  }

  $scope.cancelAddSupply = function(index) {
    $scope.consignment.supplies.splice(index, 1);
  }

  $scope.cancelAddCharge = function(index) {
    $scope.consignment.charges.splice(index, 1);
  }

  $scope.removeItem = function(index) {
    $scope.consignment.items.splice(index, 1);
  }

  $scope.removeSupply = function(index) {
    $scope.consignment.supplies.splice(index, 1);
  }

  $scope.removeCharge = function(index) {
    $scope.consignment.charges.splice(index, 1);
  }

  $scope.volumetricWeight = function(index) {

    var item = $scope.consignment.items[index];
    var l = parseFloat(item.length);
    var w = parseFloat(item.width);
    var h = parseFloat(item.height);

    if ($scope.consignment.mode === 'Road Express') {
        return parseFloat(item.dead_weight);
    }
    else if ($scope.consignment.mode === 'Perishable Air') {
        return (l * w * h) / 6000;
    }
    else {
        return (l * w * h) / 5000;
    }

  }

  $scope.chargeableWeight = function(index) {
    var item = $scope.consignment.items[index];
    var volumetric_weight = $scope.volumetricWeight(index);
    if (volumetric_weight > item.dead_weight) {
        return volumetric_weight;
    }
    else {
        return parseFloat(item.dead_weight);
    }
  }

  // Line total.
  $scope.total = function(index) {
    var charge = $scope.consignment.charges[index];
    var cost = parseFloat(charge.cost);
    var qty = parseFloat(charge.quantity);
    return cost * qty;
  }

  // Grand total.
  $scope.grandTotal = function() {
    var grandTotal = 0.0;
    for (i=0; i<$scope.consignment.charges.length; i++) {
        grandTotal += $scope.total(i);
    }
    return grandTotal;
  }

  $scope.calculateETA = function() {

    if ($scope.consignment.mode == "Overnight Air") {
        var eta = new moment($scope.consignment.pickupDate)
                    .add("days", 1)
                    .startOf("day")
                    .add("hours", 9);
        $scope.consignment.eta_date = eta.format("DD-MMM-YYYY hh:mm");
    }
  }

  $scope.formatAddress = function(entity) {
    return EntityHelper.formattedAddress(entity);
  }

  $scope.openPickupDate = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.opened_pickup = true;
  }

  $scope.openETADate = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.opened_eta = true;
  }

}]);

