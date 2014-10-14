lc.controller("ConsignmentController", ['$scope', '$rootScope', '$location', '$localStorage', 'ConsignmentService', 'EntityHelper', 'consignment', 'entities', function($scope, $rootScope, $location, $localStorage, ConsignmentService, EntityHelper, consignment, entities) {

  $rootScope.activeMenu = "Consignments";
  $rootScope.currentUser = $localStorage.user;

  $scope.promise = null;
  $scope.message = "";

  $scope.alert = {
    "show": false,
    "title": "",
    "message": ""
  }

  $scope.onConsignorChange = function(entityId) {
    $scope.entities.forEach(function(entity) {
        console.log("ok2");
        if (entity.id == entityId) {
            console.log("ok3");
            setTimeout(function() {
                $scope.consignment.account = entity.name;
                $scope.selectedConsignor = entity;
            }, 10);
        }
    });
  }

  $scope.onConsigneeChange = function(entityId) {
    $scope.entities.forEach(function(entity) {
        if (entity.id == entityId) {
            setTimeout(function() {
                $scope.selectedConsignee = entity;
            }, 10);
        }
    });
  }

  $scope.entities = entities;
  $scope.consignment = consignment;
  if ($scope.consignment) {
    $scope.onConsignorChange($scope.consignment.consignor);
    $scope.onConsigneeChange($scope.consignment.consignee);
    $scope.isNew = false;
  }
  else {
    $scope.consignment = {}
    $scope.isNew = true;
  }

  $scope.selectedConsignor = {}
  $scope.selectedConsignee = {}

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
    'Same Day',
    'Overnight',
    'Next Flight'
  ];

  $scope.save = function() {
    if ($scope.isNew) {
        $scope.message = "Adding ...";
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
        "weight": "0.0",
        "temp": "",
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

  $scope.doneAddCharge = function(index) {
    $scope.consignment.charges[index].isNew = false;
  }

  $scope.cancelAddItem = function(index) {
    $scope.consignment.items.splice(index, 1);
  }

  $scope.cancelAddCharge = function(index) {
    $scope.consignment.charges.splice(index, 1);
  }

  $scope.removeItem = function(index) {
    $scope.consignment.items.splice(index, 1);
  }

  $scope.removeCharge = function(index) {
    $scope.consignment.charges.splice(index, 1);
  }

  $scope.total = function(index) {
    var charge = $scope.consignment.charges[index];
    var cost = parseFloat(charge.cost);
    var qty = parseFloat(charge.quantity);
    return cost * qty;
  }

  $scope.grandTotal = function() {
    var grandTotal = 0.0;
    for (i=0; i<$scope.consignment.charges.length; i++) {
        grandTotal += $scope.total(i);
    }
    return grandTotal;
  }

  $scope.formatAddress = function(entity) {
    return EntityHelper.formattedAddress(entity);
  }

  $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.opened = true;
  }

}]);

