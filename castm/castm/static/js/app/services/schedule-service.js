castM.factory("ScheduleService", function($http, $q, $localStorage) {
    var api_url = "/api/events/"
    return {
        getSchedules: function(eventId) {
            var url = api_url + eventId + "/schedules/";
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
        getSchedule: function(eventId, scheduleId) {
            var url = api_url + eventId + "/schedules/" + scheduleId + "/";
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
        addSchedule: function(eventId, schedule) {
            var url = api_url + eventId + "/schedules/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'POST',
                url: url,
                data: schedule
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        updateSchedule: function(eventId, scheduleId, schedule) {
            var url = api_url + eventId + "/schedules/" + scheduleId + "/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'PUT',
                url: url,
                data: schedule
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        removeSchedule: function(eventId, scheduleId) {
            var url = api_url + eventId + "/schedules/" + scheduleId + "/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'DELETE',
                url: url
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        addAttendee: function(eventId, scheduleId, attendee) {
            var url = api_url + eventId + "/schedules/" + scheduleId + "/attendees/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'POST',
                url: url,
                data: attendee
            }).success(function(data, status, header, config) {
                defer.resolve(data);
            }).error(function(data, status, header, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        removeAttendee: function(eventId, scheduleId, attendeeId) {
            var url = api_url + eventId + "/schedules/" + scheduleId + "/attendees/" + attendeeId + "/";
            var defer = $q.defer();
            $http({
                headers: {
                    'Authorization': 'Token ' + $localStorage.user.token
                },
                method: 'DELETE',
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