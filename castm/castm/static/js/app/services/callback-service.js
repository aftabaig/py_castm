castM.factory("CallbackService", function($http, $q, $localStorage) {
    var api_url = "/api/events/"
    return {
        getCallbacks: function(eventId) {
            var url = api_url + eventId + "/callbacks/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'GET',
                url: url
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        sendCallbacks: function(eventId, callbacks) {
            var url = api_url + eventId + "/schedules/" + scheduleId + "/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'PUT',
                url: url,
                data: callbacks
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        }
    }
});