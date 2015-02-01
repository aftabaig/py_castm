castM.controller("ScheduleController", ['$scope', '$rootScope', '$location', '$localStorage', 'ScheduleService', 'event', 'schedules', 'talentAttendees', function($scope, $rootScope, $location, $localStorage, ScheduleService, event, schedules, talentAttendees) {

    $scope.event = event;
    $scope.schedules = schedules;
    $scope.calEntries = [];
    $scope.talentAttendees = talentAttendees;
    $scope.newSchedule = {}

    $scope.alertOnDrop = function(event, delta, revertFunc, jsEvent, ui, view){
       console.log("in alertOnDrop");
       console.dir(event);
    };

    $scope.uiConfig = {
        calendar:{
            height: 450,
            editable: true,
            header:{
                left: 'title',
                center: '',
                right: 'today prev,next'
            },
            eventClick: $scope.alertOnEventClick,
            eventDrop: $scope.alertOnDrop,
            eventResize: $scope.alertOnResize,
            eventRender: $scope.eventRender
        }
    };

    $scope.toCalendar = function(schedule) {
        return {
            title: schedule.schedule_title,
            start: schedule.schedule_time_from,
            end: schedule.schedule_time_to,
            allDay: false
        }
    }

    $scope.init = function() {
        $scope.schedules.forEach(function(schedule) {
            schedule.schedule_time_from = moment(schedule.schedule_time_from).format("hh:mm a")
            schedule.schedule_time_to = moment(schedule.schedule_time_to).format("hh:mm a")
            $scope.calEntries.push({
                id: schedule.schedule_id,
                title: schedule.schedule_title,
                start: new Date(2015, 1, 29, 5, 0),
                end: new Date(2015, 1, 29, 7, 0),
                allDay: false
            });
        });
        $scope.calEntries = [$scope.calEntries];
    }
    console.dir($scope.calEntries);
    $scope.init();

    $scope.addNewSchedule = function() {

        var schedule = $scope.newSchedule;
        schedule.schedule_date = moment().format('YYYY-MM-DD');
        schedule.schedule_time_from = moment(12, "HH").format("HH:mm");
        schedule.schedule_time_to = moment(14, "HH").format("HH:mm");

        console.dir(schedule);

        ScheduleService.addSchedule(event.event_id, schedule)
        .then(function(addedSchedule) {
        }, function(error) {

        })

    }

}]);