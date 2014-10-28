lc.factory("SearchService", function($http, $q, $localStorage) {
    var api_url = "/api/searches/";
    return {
        info: function(searchId) {
            var url = api_url + searchId + "/";
            var defer = $q.defer();
            $http({
                method: 'GET',
                url: url
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        all: function() {
            var defer = $q.defer();
            $http({
                method: 'GET',
                url: api_url
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        add: function(search) {
            var defer = $q.defer();
            console.log("search");
            console.dir(search);
            $http({
                method: 'POST',
                url: api_url,
                data: search
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        update: function(search) {
            var url = api_url + search.id + "/";
            var defer = $q.defer();
            $http({
                method: 'PUT',
                url: url,
                data: entity
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        delete: function(search_id) {
            var url = api_url + search_id + "/";
            var defer = $q.defer();
            $http({
                method: 'DELETE',
                url: url
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
    }
});