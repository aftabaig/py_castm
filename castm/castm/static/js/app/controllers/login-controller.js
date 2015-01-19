castM.controller("LoginController", ['$scope', '$rootScope', '$location', '$localStorage', 'UserService', function($scope, $rootScope, $location, $localStorage, UserService) {

    $scope.doLogin = function() {

        UserService.authenticate($scope.emailAddress, $scope.password)
        .then(function(user) {
            /*
            {
                "token": "b95175a8e01d3ac718d12669f1ca8ddd37bf6f3d",
                "type": 'C',
                "sub_type": ''
            }
            */
            console.dir(user);
            if (user.type != 'C') {
                $scope.errorMessage = "The web app is currently designed for the casting users only.";
            }
            else {
                $localStorage.user = user;
                $location.path("/home")
            }
        }, function(error) {
            /*
            {
                "code": [400],
                "message": [message]
            }
            */
            $scope.errorMessage = error.message;
            $scope.emailAddress = "";
            $scope.password = "";
        });

    }

}]);