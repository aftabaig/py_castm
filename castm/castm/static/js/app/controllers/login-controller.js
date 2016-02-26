castM.controller("LoginController", ['$scope', '$rootScope', '$location', '$localStorage', 'UserService', function($scope, $rootScope, $location, $localStorage, UserService) {

    $scope.doLogin = function() {

        $scope.errorMessage = "";

        UserService.authenticate($scope.emailAddress, $scope.password)
        .then(function(user) {
            /*
            {
                "token": "b95175a8e01d3ac718d12669f1ca8ddd37bf6f3d",
                "type": 'C'
            }
            */
            if (user.type != 'C') {
                $scope.errorMessage = "The web app is currently designed for the casting users only. For access, search your app store for CastM";
            }
            else {
                console.log(user);
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
