(function(){
    var app = angular.module('metric-comments', ['ngCookies']);
    app.config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    });
    app.run(['$http', '$cookies', function ($http, $cookies) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    }]);
    app.controller('CommentsController', ['$scope', '$http', function($scope, $http){
        var pattern = /\/metric\/(\d+)/;
        var metric_id = location.href.match(pattern)[1];
        $scope.comment_text = "";
        $scope.comments = [];
        $scope.reload_comments = function() {
            $http.get('/api/metrics/' + metric_id + "/comments/")
                .success(function (data) {
                    $scope.comments = [];
                    $scope.comments.push.apply($scope.comments, data);
                    $("#comments").scrollTop($("#comments")[0].scrollHeight);
                });
        };
        $scope.reload_comments();
        $scope.add_a_comment = function() {
            $http.post('/api/metrics/' + metric_id + "/comments/", {'text': $scope.comment_text})
                .success(function (data) {
                    //$scope.comments = [];
                    $scope.comments.push(data);
                    $scope.comment_text = "";
                    $("#comments").scrollTop($("#comments")[0].scrollHeight);
                });
        };



        
    }]);

})();