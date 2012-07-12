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
    $scope.save = function() {
        list = [];
        for (var name in $scope.checkins)
            list.push({'name':name, 'weight':$scope.checkins[name]});
        $http.post('checkin', data=list).success(function() {
            $scope.checkins = {};
        });
    }
}

function ClubCtrl($scope, $http, $routeParams, $location) {
    $scope.name = $routeParams.name;

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
}

