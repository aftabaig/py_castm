castM.controller("CallbackController", ['$scope', '$rootScope', '$location', '$localStorage', 'CallbackService', 'event', 'callbacks', function($scope, $rootScope, $location, $localStorage, CallbackService, event, callbacks) {

    $scope.event = event;
    $scope.callbacks = callbacks;

    $scope.getCallbackType = function(abbr) {
        if (abbr === 'HCB') {
            return "Headshot/Resume Callback";
        }
        else if (abbr === 'DCB') {
            return 'Dancer Callback';
        }
        else {
            return 'Regular Callback';
        }
    }

    
}]);