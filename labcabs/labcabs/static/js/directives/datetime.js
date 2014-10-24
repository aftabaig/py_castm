lc.directive('datetime', function () {
    return function (scope, element, attrs) {
        console.dir(element);
        console.dir(attrs);
        $(element).datetimepicker({
            format: "d-M-Y h:m",
            todayButton: true,
            closeOnDateSelect: true
        });
    };
});