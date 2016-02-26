castM.factory("BroadcastService", function($http, $q, $localStorage) {
    var api_url = "/api/events/"
    return {
        broadcast: function(eventId, to, message) {
            var url = api_url + eventId + "/broadcast/";
            var defer = $q.defer();
            $http({
                method: 'POST',
                url: url,
                data: {
                    "to": to,
                    "title": "",
                    "message": message
                }
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(data);
            });
            return defer.promise;
        }
    }
});