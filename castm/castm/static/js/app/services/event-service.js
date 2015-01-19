castM.factory("EventService", function($http, $q, $localStorage) {
    return {
        eventDetail: function(eventId) {
            var url = "/api/events/" + eventId + "/";
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
        allTalentAttendees: function(eventId) {
            var url = "/api/events/" + eventId + "/attendees/";
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
        approvedTalentAttendees: function(eventId) {
            var url = "/api/events/" + eventId + "/attendees/approved/";
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
        pendingTalentAttendees: function(eventId) {
            var url = "/api/events/" + eventId + "/attendees/pending/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'GET',
                url: url,
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(data);
            });
            return defer.promise;
        },
        allCastingAttendees: function(eventId) {
            var url = "/api/events/" + eventId + "/casting/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'GET',
                url: url,
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(data);
            });
            return defer.promise;
        },
        approvedCastingAttendees: function(eventId) {
            var url = "/api/events/" + eventId + "/casting/approved/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'GET',
                url: url,
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(data);
            });
            return defer.promise;
        },
        pendingCastingAttendees: function(eventId) {
            var url = "/api/events/" + eventId + "/casting/pending/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'GET',
                url: url,
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(data);
            });
            return defer.promise;
        },
        acceptRequest: function(eventId, requestId) {
            var url = "/api/events/" + eventId + "/requests/" + requestId + "/accept/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'PUT',
                url: url,
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(data);
            });
            return defer.promise;
        },
        rejectRequest: function(eventId, requestId) {
            var url = "/api/events/" + eventId + "/requests/" + requestId + "/reject/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'PUT',
                url: url,
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(data);
            });
            return defer.promise;
        }
    }
});