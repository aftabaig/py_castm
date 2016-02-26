castM.service('Interceptor', function($localStorage) {
    console.log("<<<<>>>>>");
    var service = this;
    service.request = function(config) {
        var user = $localStorage.user;
        console.log(user);
        if (user) {
            config.headers.Authorization = "Token " + user.token;
        }
        return config;
    };
});
