castM.controller("CallbackController", ['$scope', '$rootScope', '$location', '$localStorage', 'CallbackService', 'event', 'callbacks', function($scope, $rootScope, $location, $localStorage, CallbackService, event, callbacks) {

    $scope.event = event;
    $scope.callbacks = callbacks;
    $scope.searchQuery = "";

    $scope.callbacks = []
    callbacks.forEach(function(callback) {
        callback.talent_callbacks.forEach(function(talent_callback) {
            talent_callback.callback_organization_name = callback.callback_organization_name;
            $scope.callbacks.push(talent_callback)
        })

    })
    $scope.currentCallbacks = angular.copy($scope.callbacks);

    $scope.currentPage = 0;
    $scope.pageSize = 30;
    $scope.pageCount = function() {
        return Math.ceil($scope.currentCallbacks.length/$scope.pageSize);
    }

    $scope.nextPage = function() {
        if ($scope.currentPage < $scope.pageCount()-1) {
            $scope.currentPage++;
        }
    }

    $scope.prevPage = function() {
        if ($scope.currentPage > 0) {
            $scope.currentPage--;
        }
    }

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

    $scope.search = function() {
        $scope.currentCallbacks = [];
        $scope.currentPage = 0;
        $scope.callbacks.forEach(function(callback) {
            var queryParts = $scope.searchQuery.split(' ');
            queryParts.forEach(function(part) {
                var re = new RegExp(part, 'i');
                var match1 = callback.callback_organization_name.match(re);
                var match2 = callback.talent_first_name.match(re);
                var match3 = callback.talent_last_name.match(re);
                var match4 = callback.talent_audition_id.match(re);
                var match5 = $scope.getCallbackType(callback.callback_type).match(re);
                if (match1 || match2 || match3 || match4 || match5) {
                    $scope.currentCallbacks.push(callback);
                }
            })
        });
        $scope.sortBy($scope.sortParameter);

    }

    $scope.sortBy = function(param) {
        if (param === 'organization') {
            $scope.currentCallbacks.sort(function(callback1, callback2) {
                if (callback1.callback_organization_name < callback2.callback_organization_name) {
                    return -1;
                }
                if (callback1.callback_organization_name > callback2.callback_organization_name) {
                    return 1;
                }
                return 0;
            });
        }
        else if (param === 'talent') {
            $scope.currentCallbacks.sort(function(callback1, callback2) {
                if (callback1.talent_last_name < callback2.talent_last_name) {
                    return -1;
                }
                if (callback1.talent_last_name > callback2.talent_last_name) {
                    return 1;
                }
                return 0;
            });
        }
        else if (param === 'audition_num') {
            $scope.currentCallbacks.sort(function(callback1, callback2) {
                audition_id1 = parseInt(callback1.talent_audition_id);
                audition_id2 = parseInt(callback2.talent_audition_id);
                if (audition_id1 < audition_id2) {
                    return -1;
                }
                if (audition_id1 > audition_id2) {
                    return 1;
                }
                return 0;
            });
        }
        else if (param === 'callback_type') {
            $scope.currentCallbacks.sort(function(callback1, callback2) {
                if (callback1.callback_type < callback2.callback_type) {
                    return -1;
                }
                if (callback1.callback_type > callback2.callback_type) {
                    return 1;
                }
                return 0;
            });
        }
        $scope.sortParameter = param;
    }
    $scope.sortBy("last-name");

}]);