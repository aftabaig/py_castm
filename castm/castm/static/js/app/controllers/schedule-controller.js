castM.controller("ScheduleController", ['$scope', '$rootScope', '$location', '$localStorage', 'ScheduleService', 'event', 'schedules', function($scope, $rootScope, $location, $localStorage, ScheduleService, event, schedules) {

    $scope.event = event;
    $scope.schedules = schedules;
    $scope.newSchedule = {}

    schedules.forEach(function (schedule) {
        schedule.schedule_date = new Date(schedule.schedule_date)
        schedule.schedule_time_from = new Date(schedule.schedule_time_from)
        schedule.schedule_time_to = new Date(schedule.schedule_time_to)
    })

    // Clears the new schedule.
    // Called after a new schedule is added.
    $scope.clear = function() {
        $scope.newSchedule = {}
    }

    $scope.validate = function(schedule) {

        console.dir(schedule);

        if (!schedule.schedule_title || schedule.schedule_title.length == 0) {
            $scope.message = "Session title cannot be empty";
            return false;
        }
        if (!schedule.schedule_date || schedule.schedule_date.length == 0) {
            $scope.message = "Session date cannot be empty";
            return false;
        }
        if (!schedule.schedule_time_from || schedule.schedule_time_from.length == 0) {
            $scope.message = "Session time cannot be empty";
            return false;
        }
        if (!schedule.schedule_time_to || schedule.schedule_time_to.length == 0) {
            $scope.message = "Session time cannot be empty";
            return false;
        }

        $scope.message = "";
        return true;

    }

    $scope.addNewSession = function() {

        var schedule = $scope.newSchedule;

        if (!$scope.validate(schedule)) {
            return;
        }

        schedule.schedule_date = moment(schedule.schedule_date).format("YYYY-MM-DD")
        schedule.schedule_time_from = moment(schedule.schedule_time_from).format("HH:mm")
        schedule.schedule_time_to = moment(schedule.schedule_time_to).format("HH:mm")

        $scope.updating = true;

        ScheduleService.addSchedule(event.event_id, schedule)
        .then(function(addedSchedule) {

            $scope.newSchedule = {}
            console.dir(addedSchedule);
            schedule.schedule_id = addedSchedule.schedule_id;
            schedule.schedule_date = new Date(addedSchedule.schedule_date);
            schedule.schedule_time_from = new Date(addedSchedule.schedule_time_from);
            schedule.schedule_time_to = new Date(addedSchedule.schedule_time_to);
            $scope.schedules.push(schedule);

            $scope.updating = false;
            $scope.message = "";

        }, function(error) {

            $scope.updating = false;
            $scope.message = error.message;

        })

    }

    $scope.updateSession = function(index) {

        var schedule = $scope.schedules[index];

        if (!$scope.validate(schedule)) {
            return;
        }

        schedule.schedule_date = moment(schedule.schedule_date).format("YYYY-MM-DD")
        schedule.schedule_time_from = moment(schedule.schedule_time_from).format("HH:mm")
        schedule.schedule_time_to = moment(schedule.schedule_time_to).format("HH:mm")

        ScheduleService.updateSchedule(event.event_id, schedule.schedule_id, schedule)
        .then(function(updatedSchedule) {

            schedule.schedule_date = new Date(addedSchedule.schedule_date);
            schedule.schedule_time_from = new Date(addedSchedule.schedule_time_from);
            schedule.schedule_time_to = new Date(addedSchedule.schedule_time_to);

            $scope.updating = false;
            $scope.message = "";

        }, function(error) {
            $scope.updating = false;
            $scope.message = error.message;
        })
    }

    $scope.removeSession = function(index) {

        var schedule = $scope.schedules[index];
        if (schedule) {

            $scope.message = "";
            $scope.updating = true;

            console.dir(schedule)
            console.dir(event)

            ScheduleService.removeSchedule(schedule.event_id, schedule.schedule_id)
            .then(function() {
                console.log("ok")
                $scope.schedules.splice(index, 1);
                $scope.updating = false;
            }, function(error) {
                $scope.updating = false;
                if (error.message) {
                    $scope.message = error.message;
                }
                else {
                    $scope.message = "Could not delete, please try again later."
                }
            })

        }

    }

}]);