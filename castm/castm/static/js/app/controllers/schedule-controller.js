castM.controller("ScheduleController", ['$scope', '$rootScope', '$modal', '$location', '$localStorage', 'ScheduleService', 'event', 'schedules', function($scope, $rootScope, $modal, $location, $localStorage, ScheduleService, event, schedules) {

    $scope.init = function() {
        $scope.event = event;
        $scope.schedules = schedules;

        schedules.forEach(function (schedule) {
            schedule.schedule_date = new Date(schedule.schedule_date)
            schedule.schedule_time_from = new Date(schedule.schedule_time_from)
            schedule.schedule_time_to = new Date(schedule.schedule_time_to)
        })
    }
    $scope.init();

    $scope.editSession = function(sessionIndex, talentIndex) {

        var modalInstance = $modal.open({
            templateUrl: "static/js/app/views/casting/popups/talent-sessions-popup.html",
            controller: function($scope, $modalInstance, $state, event, talent, sessions, currentSession, ScheduleService) {
                $scope.event = event;
                $scope.talent = talent;
                $scope.sessions = sessions;
                $scope.currentSession = currentSession;
                console.dir($scope.currentSession);
                console.dir($scope.sessions);
                $scope.setAsCurrentSession = function(index) {
                    $scope.currentSession = $scope.sessions[index];
                }
                $scope.ok = function() {
                    ScheduleService.addAttendee($scope.event.event_id, $scope.currentSession.schedule_id, {
                        "schedule_id": $scope.currentSession.schedule_id,
                        "attendee_id": $scope.talent.attendee_id
                    }).then(function(data) {
                        $modalInstance.dismiss('done');
                        $state.reload();
                    }, function(error) {
                        $modalInstance.dismiss('cancel');
                    });
                }
                $scope.cancel = function() {
                    $modalInstance.dismiss('cancel');
                }
            },
            resolve: {
                event: function() {
                    return $scope.event;
                },
                talent: function() {
                    return $scope.schedules[sessionIndex].attendees[talentIndex];
                },
                sessions: function() {
                    return $scope.schedules;
                },
                currentSession: function(ScheduleService) {
                    return $scope.schedules[sessionIndex];
                }
            }
        }).result;

    }

    $scope.editAuditionNum = function(sessionIndex, talentIndex) {

        var modalInstance = $modal.open({
            templateUrl: "static/js/app/views/casting/popups/edit-audition-num-popup.html",
            controller: function($scope, $modalInstance, $location, event, talent, EventService) {
                $scope.event = event;
                $scope.talent = talent;
                $scope.ok = function() {
                    EventService.changeTalentAuditionId($scope.event.event_id, $scope.talent.attendee_id, $scope.new_audition_num)
                    .then(function(status) {
                        $scope.talent.attendee_audition_id = $scope.new_audition_num;
                        $modalInstance.close('done');
                    }, function(error) {
                        $modalInstance.dismiss("cancel");
                    })
                }
                $scope.cancel = function() {
                    $modalInstance.dismiss('cancel');
                }
            },
            resolve: {
                event: function() {
                    return $scope.event;
                },
                talent: function() {
                    return $scope.schedules[sessionIndex].attendees[talentIndex];
                }
            }
        }).result;


    }

}]);