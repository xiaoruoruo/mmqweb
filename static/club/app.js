angular.module('club', []).
    config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/', {templateUrl: '/static/club/member-list.html', controller: ClubCtrl}).
        when('/checkin/:name', {templateUrl: '/static/club/member-checkin.html', controller: ClubCtrl}).
        otherwise({redirectTo: '/'});
}]);

function OutCtrl($scope, $http) {
    $http.get('api/member/?format=json').success(function(data) {
        $scope.members = data.objects;
    });
    $scope.checkins = {};
    $scope.server_message = "";
    $scope.save = function() {
        list = [];
        for (var name in $scope.checkins)
            list.push({'name':name, 'weight':$scope.checkins[name]});
        $http.post('checkin', data=list).success(function() {
            $scope.checkins = {};
            $scope.server_message = "保存成功！"
        });
    }

    $scope.add_member = function(name, is_girl, cb) {
        // TODO prevent adding an existing member (same name)
        $http.post('new_member', JSON.stringify({'name': name, 'male': !is_girl}))
             .success(function() {
                 $scope.members.push({'name': name});
                 cb();
              });
    }
}

function ClubCtrl($scope, $http, $routeParams, $location) {
    $scope.name = $routeParams.name;
    $scope.girl_new_member = false;

    $scope.doFilter = function(elem) {
        if (!$scope.query) return true;
        return angular.lowercase(elem.index).indexOf(angular.lowercase($scope.query)) == 0;
    }

    $scope.checkin = function(name, weight) {
        $scope.checkins[name] = weight;
        $location.path('/');
    }

    $scope.isCheckin = function(member) {
        return !! $scope.checkins[member.name];
    }

    $scope.new_member = function(do_checkin) {
        console.log(do_checkin);
        var name = $scope.name_new_member;
        var is_girl = $scope.girl_new_member;
        $scope.add_member(name, is_girl, function () {
            if (do_checkin) {
                $location.path('/checkin/' + name);
            }
        });
    }
}

