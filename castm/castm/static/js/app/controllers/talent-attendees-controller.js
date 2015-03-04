castM.controller("TalentAttendeesController", ['$scope', '$rootScope', '$modal', '$location', '$localStorage', 'EventService', 'event', 'talentAttendees', function($scope, $rootScope, $modal, $location, $localStorage, EventService, event, talentAttendees) {

    $scope.event = event;
    $scope.talentAttendees = talentAttendees;
    $scope.currentAttendees = angular.copy(talentAttendees);
    $scope.searchQuery = "";

    $scope.currentPage = 0;
    $scope.pageSize = 30;
    $scope.pageCount = function() {
        return Math.ceil($scope.currentAttendees.length/$scope.pageSize);
    }

    $scope.acceptRequest = function(index, isTalent) {

        // Get reference to attendee.
        var attendee = $scope.currentAttendees[index];

        attendee.updating = true;

        // Send "accept" request to server.
        EventService.acceptRequest(event.event_id, attendee.attendance_id)
        .then(function(data) {
            attendee.updating = false;
            attendee.is_accepted = true;
            attendee.is_rejected = false;
        }, function(error) {
            attendee.updating = false;
            attendee.message = error.message;
        });

    }

    $scope.rejectRequest = function(index, isTalent) {

        // Get reference to attendee.
        var attendee = $scope.talentAttendees[index];

        attendee.updating = true;

        // Send "reject" request to server.
        EventService.rejectRequest(event.event_id, attendee.attendance_id)
        .then(function(data) {
            attendee.updating = false;
            attendee.is_accepted = false;
            attendee.is_rejected = true;
        }, function(error) {
            attendee.updating = false;
            attendee.message = error.message;
        });

    }

    $scope.nextPage = function() {
        if ($scope.currentPage < $scope.pageCount()-1) {
            $scope.currentPage++;
        }
    }

    $scope.prevPage = function() {
        if ($scope.currentPage > 0) {
            $scope.currentPage--;
        }
    }

    $scope.setCurrentPage = function(pageNum) {
        $scope.currentPage = pageNum;
    }

    $scope.search = function() {
        $scope.currentAttendees = [];
        $scope.currentPage = 0;
        $scope.talentAttendees.forEach(function(attendee) {
            var queryParts = $scope.searchQuery.split(' ');
            queryParts.forEach(function(part) {
                var re = new RegExp(part, 'i');
                var match1 = attendee.attendee_first_name.match(re);
                var match2 = attendee.attendee_last_name.match(re);
                var match3 = attendee.attendee_title.match(re);
                var match4 = attendee.attendee_audition_id.match(re);
                if (match1 || match2 || match3 || match4) {
                    $scope.currentAttendees.push(attendee);
                }
            })
        });
        $scope.sortBy($scope.sortParameter);

    }

    $scope.sortBy = function(param) {
        if (param === 'first-name') {
            $scope.currentAttendees.sort(function(talent1, talent2) {
                if (talent1.attendee_first_name < talent2.attendee_first_name) {
                    return -1;
                }
                if (talent1.attendee_first_name > talent2.attendee_first_name) {
                    return 1;
                }
                return 0;
            });
        }
        else if (param === 'last-name') {
            $scope.currentAttendees.sort(function(talent1, talent2) {
                if (talent1.attendee_last_name < talent2.attendee_last_name) {
                    return -1;
                }
                if (talent1.attendee_last_name > talent2.attendee_last_name) {
                    return 1;
                }
                return 0;
            });
        }
        else if (param == 'audition-num') {
            $scope.currentAttendees.sort(function(talent1, talent2) {
                audition_id1 = parseInt(talent1.attendee_audition_id);
                audition_id2 = parseInt(talent2.attendee_audition_id);
                if (audition_id1 < audition_id2) {
                    return -1;
                }
                if (audition_id1 > audition_id2) {
                    return 1;
                }
                return 0;
            });
        }
        $scope.sortParameter = param;
    }
    $scope.sortBy("last-name");

    $scope.filterBy = function(param) {
        if (param == '') {
            $scope.currentAttendees = angular.copy($scope.talentAttendees);
        }
        else if (param == 'un-approved') {
            $scope.currentAttendees = [];
            $scope.talentAttendees.forEach(function(attendee) {
                if (!attendee.is_accepted && !attendee.is_rejected) {
                    $scope.currentAttendees.push(attendee);
                }
            })
        }
        else if (param == 'un-assigned') {
            $scope.currentAttendees = [];
            $scope.talentAttendees.forEach(function(attendee) {
                if (!attendee.attendee_audition_id) {
                    $scope.currentAttendees.push(attendee);
                }
            })
        }
        $scope.filterParameter = param;
        $scope.sortBy($scope.sortParameter);
    }
    $scope.filterBy("");

    $scope.openSessions = function(index) {

        var modalInstance = $modal.open({
            templateUrl: "static/js/app/views/casting/popups/talent-sessions-popup.html",
            controller: function($scope, $modalInstance, event, talent, sessions, currentSession, ScheduleService) {
                sessions.forEach(function(session) {
                    session.schedule_date = new Date(session.schedule_date)
                    session.schedule_time_from = new Date(session.schedule_time_from)
                    session.schedule_time_to = new Date(session.schedule_time_to)
                })
                $scope.event = event;
                $scope.talent = talent;
                $scope.sessions = sessions;
                $scope.currentSession = currentSession;
                $scope.setAsCurrentSession = function(index) {
                    $scope.currentSession = $scope.sessions[index];
                }
                $scope.ok = function() {
                    ScheduleService.addAttendee($scope.event.event_id, $scope.currentSession.schedule_id, {
                        "schedule_id": $scope.currentSession.schedule_id,
                        "attendee_id": $scope.talent.attendee_id
                    }).then(function(data) {
                        $modalInstance.dismiss('cancel');
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
                    return $scope.currentAttendees[index];
                },
                sessions: function(ScheduleService) {
                    return ScheduleService.getSchedules($scope.event.event_id);
                },
                currentSession: function(ScheduleService) {
                    return ScheduleService.getTalentSchedule($scope.event.event_id, $scope.currentAttendees[index].attendee_id);
                }
            }
        }).result;

    }

    $scope.deleteUserSession = function(index) {

        var modalInstance = $modal.open({
            templateUrl: "static/js/app/views/casting/popups/delete-session-confirmation-popup.html",
            controller: function($scope, $modalInstance, event, talent, currentSession, ScheduleService) {
                $scope.event = event;
                $scope.talent = talent;
                $scope.currentSession = currentSession;
                $scope.ok = function() {
                    ScheduleService.removeAttendee($scope.event.event_id, $scope.currentSession.schedule_id, $scope.currentSession.attendance_id)
                    .then(function(status) {
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
                    return $scope.currentAttendees[index];
                },
                currentSession: function(ScheduleService) {
                    return ScheduleService.getTalentSchedule($scope.event.event_id, $scope.currentAttendees[index].attendee_id);
                }
            }
        }).result;


    }

}]);