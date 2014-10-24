lc.factory("ConsignmentService", function($http, $q, $localStorage) {
    var api_url = "/api/consignments/";
    return {
        info: function(consignmentId) {
            var url = api_url + consignmentId;
            var defer = $q.defer();
            $http({
                method: 'GET',
                url: url
            }).success(function(data, status, header, config) {
                console.log("data");
                console.dir(data);
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        email: function(consignmentId, entity) {
            var data = {
                "entity": entity
            }
            var defer = $q.defer();
            $http({
                method: 'POST',
                url: api_url + consignmentId + "/send_as_email/",
                data: data
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
        add: function(consignment) {
            var defer = $q.defer();
            $http({
                method: 'POST',
                url: api_url,
                data: consignment
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        update: function(consignment) {
            console.log("consignment:");
            console.dir(consignment);
            var url = api_url + consignment.id + "/";
            var defer = $q.defer();
            $http({
                method: 'PUT',
                url: url,
                data: consignment
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        delete: function(consignment_id) {
            var url = api_url + consignment_id + "/";
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