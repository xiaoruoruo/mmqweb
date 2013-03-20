angular.module('club', ['ui']).
    config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/', {templateUrl: '/static/club/checkin.html', controller: ClubCtrl}).
        when('/checkin/:name', {templateUrl: '/static/club/member-checkin.html', controller: ClubCtrl}).
        when('/members', {templateUrl: '/static/club/members.html', controller: MemberCtrl}).
        otherwise({redirectTo: '/'});
}]);

function OutCtrl($scope, $http, $window) {
    /* hash: name -> {weight, deposit} */
    $scope.checkins = {};

    /* list: names */
    $scope.checkin_names_list = [];

    /* a local scope to make angularjs happy */
    $scope.info = {
        'query': '',
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

    $scope.get_members = function() {
        $http.get('api/member/?format=json').success(function(data) {
            $scope.members = data.objects;
        });
    }

    $scope.get_members();
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
                $scope.checkin_names_list = [];
                $scope.server_message = "保存成功！"
                $scope.get_members();
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
                 if (!_.has(data, "ok")) {
                     $scope.server_message = "保存失败？？";
                     return;
                 }
                 member = data.ok
                 $scope.server_message = "已添加会员: " + member.name;
                 $scope.members.push(member);
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

    $scope.doFilter = function(elem) {
        if (!$scope.info.query) return true;
        return angular.lowercase(elem.index).indexOf(angular.lowercase($scope.info.query)) == 0;
    }
}

function ClubCtrl($scope, $http, $routeParams, $location, $filter) {
    $scope.name = $routeParams.name;
    $scope.deposit = ($scope.checkins[$scope.name] || {})['deposit'];
    console.log("ClubCtrl");

    /* checkin using enter if only one is left */
    $scope.queryOnEnter = function() {
        var filtered = $filter('filter')($scope.members, $scope.doFilter);
        if (filtered.length == 1) {
            $scope.checkin_click(filtered[0].name);
        }
    }

    $scope.queryOnEsc = function() {
        $scope.info.query = "";
    }

    $scope.checkin_click = function(name) {
        $scope.info.query = "";
        if ($scope.isCheckin(name)) {
            $location.path('/checkin/' + name);
        } else {
            // 默认weight = 1，节省一次点击
            $scope.do_checkin(name, 1.0);
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

    $scope.isCheckin = function(name) {
        if (! $scope.checkins[name]) {
            return false;
        }
        var weight = $scope.checkins[name]['weight'];
        return weight > 0;
    }

    $scope.new_member = function(do_checkin) {
        var name = $scope.name_new_member;
        if (!name) {
            // invalid name
            return;
        }
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

    $scope.edit_member = function(member) {
        $scope.memberEdit = member;
        $('#editModal').modal();
    }

    $scope.edit_member_save = function() {
        $http.put($scope.memberEdit.resource_uri, $scope.memberEdit)
            .success(function () {
                $('#editModal').modal('hide');
            })
            .error(function () {
                alert("出错了，请稍后再试");
            }) ;
    }

    $scope.delete_member = function(member) {
        var r = confirm("确定要删除会员“" + member.name + "”吗？");
        if (r == true) {
            $http({
                method: 'PATCH', 
                url: member.resource_uri, 
                data: {'hidden': true},
                headers: {'Content-Type': 'application/json'},
            });
        }
    }
}
