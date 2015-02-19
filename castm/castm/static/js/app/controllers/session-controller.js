castM.controller("SessionController", ['$scope', '$rootScope', '$location', '$localStorage', 'ScheduleService', 'event', 'schedules', function($scope, $rootScope, $location, $localStorage, ScheduleService, event, schedules) {

    $scope.event = event;
    $scope.schedules = schedules;
    $scope.newSchedule = {}
    console.dir($scope.schedules);
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

        if (!$scope.validate($scope.newSchedule)) {
            return;
        }

        var schedule = {};
        schedule.sort_id = $scope.schedules.length + 1;
        schedule.schedule_title = $scope.newSchedule.schedule_title;
        schedule.schedule_date = moment($scope.newSchedule.schedule_date).format("YYYY-MM-DD");
        schedule.schedule_time_from = moment($scope.newSchedule.schedule_time_from).format("HH:mm");
        schedule.schedule_time_to = moment($scope.newSchedule.schedule_time_to).format("HH:mm");

        $scope.updating = true;

        ScheduleService.addSchedule(event.event_id, schedule)
        .then(function(addedSchedule) {

            $scope.newSchedule = {}
            schedule.schedule_id = addedSchedule.schedule_id;
            schedule.event_id = addedSchedule.event_id
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

        schedule.event_id = schedule.event_id.toString()
        schedule.schedule_date = moment(schedule.schedule_date).format("YYYY-MM-DD")
        schedule.schedule_time_from = moment(schedule.schedule_time_from).format("HH:mm")
        schedule.schedule_time_to = moment(schedule.schedule_time_to).format("HH:mm")
        console.dir(schedule);
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

            ScheduleService.removeSchedule(schedule.event_id, schedule.schedule_id)
            .then(function() {
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

    $scope.moveUp = function(index) {

        if (index == 0) {
            return;
        }

        var schedule1 = $scope.schedules[index];
        var schedule2 = $scope.schedules[index-1];

        $scope.message = "";
        $scope.updating = true;

        ScheduleService.changeOrder($scope.event.event_id, {
            "schedules": [{
                "schedule_id": schedule1.schedule_id,
                "sort_id": index-1
            }, {
                "schedule_id": schedule2.schedule_id,
                "sort_id": index
            }]
        })
        .then(function() {

            schedule1.sort_id = index;
            schedule2.sort_id = index + 1;

            var ordered_schedules = $scope.schedules.splice(index-1, 2, schedule1, schedule2);
            $scope.schedules = ordered_schedules;

            $scope.updating = false;
            $scope.message = "";


        }, function(error) {

            $scope.updating = false;
            $scope.mess
        })

    }

    $scope.moveDown = function(index) {

        if (index >= $scope.schedules.length) {
            return;
        }



    }

}]);