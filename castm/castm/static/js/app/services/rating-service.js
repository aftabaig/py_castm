castM.factory("RatingService", function($http, $q, $localStorage) {
    return {
        formFields: function(organizationId) {
            var url = "/api/organizations/" + organizationId + "/forms/";
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
                defer.reject(data);
            });
            return defer.promise;
        },
        addField: function(organizationId, field) {
            var url = "/api/organizations/" + organizationId + "/forms/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'POST',
                url: url,
                data: field
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(data);
            });
            return defer.promise;
        },
        updateField: function(organizationId, field) {
            var url = "/api/organizations/" + organizationId + "/forms/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'PUT',
                url: url,
                data: field
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(data);
            });
            return defer.promise;
        },
        fieldTypes: function() {
            types = [];
            types.push({
                "key": "TXT",
                "value": "Text"
            });
            types.push({
                "key": "MUL",
                "value": "Multiline"
            });
            types.push({
                "key": "SCL",
                "value": "Scale"
            });
            types.push({
                "key": "RAD",
                "value": "Radio Button"
            });
            types.push({
                "key": "CHK",
                "value": "Checkbox"
            });
            types.push({
                "key": "DRPD",
                "value": "Dropdown"
            });
            return types;
        }
    }
});