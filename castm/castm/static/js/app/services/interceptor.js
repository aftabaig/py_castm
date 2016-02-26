castM.service('Interceptor', function(User) {
    var service = this;
    service.request = function(config) {
        var user = $localStorage.user;
        if (user) {
            config.headers.authorization = "Token " + user.token;
        }
        return config;
    };
});