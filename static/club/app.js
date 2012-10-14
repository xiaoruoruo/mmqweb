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
    $scope.checkin_count = 0;
    $scope.info = {'date': function(d) { return d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate(); } (new Date()) };
    $scope.server_message = "";
    console.log("OutCtrl");
    $scope.save = function() {
        if ($scope.checkin_count == 0) {
            $scope.server_message = "还没有点一个名不能保存";
            return;
        }
        list = [];
        for (var name in $scope.checkins)
            list.push({'name':name, 'weight':$scope.checkins[name]});
        $http.post('checkin', data={'list': list, 'date': $scope.info.date}).success(function() {
            $scope.checkins = {};
            $scope.checkin_count = 0;
            $scope.server_message = "保存成功！"
        });
    }

    $scope.add_member = function(name, is_girl, cb) {
        // prevent adding an existing member (same name)
        for (var mi in $scope.members) {
            var m = $scope.members[mi];
            if (m['name'] == name) {
                $scope.server_message = name + " 会员已在名单中，再找找";
                return;
            }
            break;
        }

        $http.post('new_member', {'name': name, 'male': !is_girl})
             .success(function() {
                 $scope.members.push({'name': name});
                 cb();
              });
    }
    
    $scope.do_checkin = function(name, weight) {
        if (!$scope.checkins[name]) {
            $scope.checkin_count ++;
            $scope.server_message = "已经点了" + $scope.checkin_count + "位会员";
        }
        $scope.checkins[name] = weight;
    }
}

function ClubCtrl($scope, $http, $routeParams, $location) {
    $scope.name = $routeParams.name;
    console.log("ClubCtrl");

    $scope.doFilter = function(elem) {
        if (!$scope.query) return true;
        return angular.lowercase(elem.index).indexOf(angular.lowercase($scope.query)) == 0;
    }

    $scope.checkin_click = function(member) {
        $scope.query = "";
        if ($scope.isCheckin(member)) {
            $location.path('/checkin/' + member.name);
        } else {
            // 默认weight = 1，节省一次点击
            $scope.do_checkin(member.name, 1.0);
        }
    }

    $scope.checkin_weight = function(name, weight) {
        $scope.do_checkin(name, weight);
        $location.path('/');
    }

    $scope.isCheckin = function(member) {
        return !! $scope.checkins[member.name];
    }

    $scope.new_member = function(do_checkin) {
        var name = $scope.name_new_member;
        var is_girl = $scope.girl_new_member == "1";
        $scope.add_member(name, is_girl, function () {
            if (do_checkin) {
                $location.path('/checkin/' + name);
            } else {
                $scope.server_message = "已添加会员 " + name;
            }
        });
    }
}

