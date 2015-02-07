castM.factory("UserService", function($http, $q, $localStorage) {
    return {
        authenticate: function(username, password) {
            var url = "/api/users/authenticate/";
            var defer = $q.defer();
            $http({
                method: 'POST',
                url: url,
                data: {
                    "username": username,
                    "password": password,
                    "device_type": "Desktop",
                }
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(data);
            });
            return defer.promise;
        },
        profile: function() {
            var url = "/api/casting/profile/";
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
        headshots: function() {
            var url = "/api/casting/headshots/";
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
        }
    }
});