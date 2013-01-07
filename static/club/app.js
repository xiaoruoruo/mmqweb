angular.module('club', []).
    config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/', {templateUrl: '/static/club/member-list.html', controller: ClubCtrl}).
        when('/checkin/:name', {templateUrl: '/static/club/member-checkin.html', controller: ClubCtrl}).
        when('/members', {templateUrl: '/static/club/members.html', controller: MemberCtrl}).
        when('/member/:name', {templateUrl: '/static/club/member_detail.html', controller: MemberCtrl}).
        otherwise({redirectTo: '/'});
}]);

function OutCtrl($scope, $http, $window) {
    $http.get('api/member/?format=json').success(function(data) {
        $scope.members = data.objects;
    });

    /* hash: name -> {weight, deposit} */
    $scope.checkins = {};

    /* list: names */
    $scope.checkin_names_list = [];

    /* a local scope to make angularjs happy */
    $scope.info = {
        'date': function(d) { return d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate(); } (new Date()),
        'member_order': "-weight",
    };

    /* shows hint messages or message from server */
    $scope.server_message = "";

    /* the style of names, just font-size now */
    $scope.member_style = {'font-size': '14px'};

    $scope.member_font_adjust = function(delta) {
        var new_size = parseInt($scope.member_style['font-size']) + delta;
        $scope.member_style['font-size'] = new_size + 'px';
    }

    $window.onbeforeunload = function() {
        if ($scope.has_unsaved_data()) {
            return "点名信息还未提交，真的要离开吗？";
        }
    }

    console.log("OutCtrl");

    $scope.has_unsaved_data = function() {
        return _.size($scope.checkins) > 0;
    }

    $scope.save = function() {
        if (!$scope.has_unsaved_data()) {
            $scope.server_message = "还没有点一个名不能保存";
            return;
        }
        list = _.map($scope.checkins, function(obj, name) {
            return _.defaults(obj, {
                'name': name,
                'deposit': null,
                'weight': null,
            });
        });
        $http.post('checkin', data={'list': list, 'date': $scope.info.date}).
            success(function(data) {
                if (data != "ok") {
                    $scope.server_message = "保存失败？？";
                    return;
                }
                $scope.checkins = {};
                $scope.server_message = "保存成功！"
            }).
            error(function(data, status) {
                if (status == 403) {
                    $scope.server_message = "请先登录！";
                } else {
                    $scope.server_message = "保存失败，程序有bug，马上就会修复。。";
                }
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
        }

        $http.post('new_member', {'name': name, 'male': !is_girl}).
             success(function(data) {
                 if (data != "ok") {
                     $scope.server_message = "保存失败？？";
                     return;
                 }
                 $scope.server_message = "已添加会员: " + name;
                 $scope.members.push({'name': name, 'weight': -1, 'index': '{'});
                 cb();
              }).
              error(function(data, status) {
                  if (status == 403) {
                      $scope.server_message = "请先登录！";
                  } else {
                      $scope.server_message = "保存失败，程序有bug，马上就会修复。。";
                  }
              });
    }
    
    $scope.do_checkin = function(name, weight) {
        if (!_.has($scope.checkins, name)) {
            $scope.checkins[name] = {};
            $scope.checkin_names_list.unshift(name);
        }
        $scope.checkins[name]['weight'] = weight;
        var sum = _.reduce(_.values($scope.checkins), function(sum, c) {return sum + c['weight'] || 0}, 0);
        $scope.server_message = "已经点了" + sum + "位会员";
    }

    $scope.do_deposit = function(name, deposit) {
        if (!_.has($scope.checkins, name)) $scope.checkins[name] = {};
        $scope.checkins[name]['deposit'] = deposit;
    }
}

function ClubCtrl($scope, $http, $routeParams, $location) {
    $scope.name = $routeParams.name;
    $scope.deposit = ($scope.checkins[$scope.name] || {})['deposit'];
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

    $scope.checkin_deposit = function(deposit) {
        deposit = Number(deposit);
        if (isNaN(deposit)) return;
        if (deposit < 0) return;
        $scope.do_deposit($scope.name, deposit);
        $location.path('/');
    }

    $scope.isCheckin = function(member) {
        if (! $scope.checkins[member.name]) {
            return false;
        }
        var weight = $scope.checkins[member.name]['weight'];
        return weight > 0;
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

    $scope.weight_style = function(w) {
        if ($scope.checkins[$scope.name]['weight'] == w) {
            return 'weight_selected';
        } else {
            return '';
        }
    }
}

function MemberCtrl($scope, $http, $routeParams, $location, $filter) {
    $scope.name = $routeParams.name;

    $scope.view_member = function(member) {
        $location.path('/member/' + member.name);
    }

    $scope.member = $filter('filter')($scope.members, {'name': $scope.name})[0];
    // call a http get for recent activities of this member.
    

}
