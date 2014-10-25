lc.factory("EntityService", function($http, $q, $localStorage) {
    var api_url = "/api/entities/";
    return {
        info: function(entityId) {
            var url = api_url + entityId;
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
        add: function(entity) {
            var defer = $q.defer();
            $http({
                method: 'POST',
                url: api_url,
                data: entity
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        update: function(entity) {
            var url = api_url + entity.id + "/";
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
        delete: function(entity_id) {
            var url = api_url + entity_id + "/";
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
        entityTypes: function() {
            var url = api_url + "entity_types/";
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
        }
    }
});

lc.factory("EntityHelper", function() {

    return {
        formattedAddress: function(entity) {
            var address = '';
            if (entity.tenancy) {
                address = address + ' ' + entity.tenancy;
            }
            if (entity.street_num) {
                address = address + ' Street # ' + entity.street_num;
            }
            if (entity.street) {
                address = address + ' ' + entity.street;
            }
            if (entity.town) {
                address = address + ' ' + entity.town;
            }
            if (entity.postcode) {
                address = address + ' ' + entity.postcode;
            }
            if (entity.state) {
                address = address + ' ' + entity.state;
            }
            if (entity.country) {
                address = address + ' ' + entity.country;
            }
            return address;
        }
    }

});