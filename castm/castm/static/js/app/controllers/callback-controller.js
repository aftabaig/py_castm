castM.controller("CallbackController", ['$scope', '$rootScope', '$location', '$localStorage', 'CallbackService', 'event', 'callbacks', function($scope, $rootScope, $location, $localStorage, CallbackService, event, callbacks) {

    $scope.event = event;
    $scope.callbacks = callbacks;

    $scope.callbacks = []
    callbacks.forEach(function(callback) {
        callback.talent_callbacks.forEach(function(talent_callback) {
            talent_callback.callback_organization_name = callback.callback_organization_name;
            $scope.callbacks.push(talent_callback)
        })

    })
    console.dir($scope.callbacks);

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