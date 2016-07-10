var app = angular.module('club', ['ui', 'ui.bootstrap']).
    config(['$routeProvider', function($routeProvider) {
    $routeProvider.
        when('/', {redirectTo: '/date/' + today()}).
        when('/date/:date', {templateUrl: '/static/club/checkin.html', controller: ClubCtrl}).
        when('/checkin/:name', {templateUrl: '/static/club/member-checkin.html', controller: ClubCtrl}).
        when('/members', {templateUrl: '/static/club/members.html', controller: MemberCtrl}).
        when('/hidden', {templateUrl: '/static/club/members-hidden.html', controller: MemberCtrl}).
        otherwise({redirectTo: '/'});
}]);

app.directive('disabler', function($compile) {
    return {
        link: function(scope, elm, attrs) {
            scope.$watch(attrs.ngModel, function(value) {
                if (value) {
                    setTimeout(function(){
                        elm.attr('disabled',true);
                    }, 0);
                } else {
                    elm.attr('disabled',false);
                }
            });
        }
    }
})

function api_error_func(data, status) {
    if (status == 403) {
        this.server_message = "请先登录！";
    } else {
        this.server_message = "保存失败，程序有bug，马上就会修复。。";
    }
    this.info.loading = false;
}

function today() {
    var d = new Date();
    return d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();
};

function OutCtrl($scope, $http, $window) {
    /* hash: name -> {weight, deposit} */
    /* weight is the same as cost in ver 2 */
    $scope.checkins = {};

    /* list: names */
    $scope.checkin_names_list = [];

    /* sum of weight */
    $scope.checkin_weight_sum = 0;

    /* a local scope to make angularjs happy */
    $scope.info = {
        'query': '',
        'date': today(),
        'member_order': "-weight",
        'loading': false,
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
        console.log("get_members");
        $http.get('api/member/?format=json').success(function(data) {
            console.log("get_members done");
            $scope.members = [];
            $scope.hidden_members = [];
            _.each(data.objects, function(member) {
                if (!member.hidden) {
                    $scope.members.push(member);
                } else {
                    $scope.hidden_members.push(member);
                }
            });
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
        $scope.info.loading = true;
        $scope.server_message = "请稍后。。。";
        list = _.map($scope.checkins, function(obj, name) {
            return _.defaults(obj, {
                'name': name,
                'deposit': null,
                'weight': null,
            });
        });
        $http.post('date/' + $scope.info.date + '/activity', data={'activities': list}).
            success(function(data) {
                if (data != "ok") {
                    $scope.server_message = "保存失败？？";
                    return;
                }
                $scope.server_message = "保存成功！"
                $scope.get_members();
                $scope.info.loading = false;
            }).
            error(function() {api_error_func.apply($scope, arguments)});
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

        $scope.info.loading = true;
        $scope.server_message = "请稍后。。。";

        $http.post('new_member', {'name': name, 'male': !is_girl}).
             success(function(data) {
                 if (!_.has(data, "ok")) {
                     $scope.server_message = "保存失败？？";
                     return;
                 }
                 member = data.ok
                 $scope.server_message = "已添加会员: " + member.name;
                 $scope.info.loading = false;
                 $scope.members.push(member);
                 cb();
              }).
            error(function() {api_error_func.apply($scope, arguments)});
    }
    
    $scope.get_activities = function(date) {
        console.log("get_activities");
        var process = function(data) {
            console.log("get_activities done");
            $scope.info.get_activities_date = date;
            $scope.checkins = {};
            $scope.checkin_names_list = [];
            $scope.checkin_weight_sum = 0;

            if (!data.activities) return;
            _.each(data.activities, function(act) {
                var name = act['name'];
                if (!_.has($scope.checkins, name)) {
                    $scope.checkins[name] = {
                        'weight': act['cost'] || 0,
                        'deposit': act['deposit'] || 0,
                    }
                    $scope.checkin_names_list.unshift(name);
                    $scope.checkin_weight_sum ++;
                } else {
                    // Merge multiple activities of the same name.
                    a = $scope.checkins[name];
                    a['weight'] += act['cost'] || 0;
                    a['deposit'] += act['deposit'] || 0;
                }
                // TODO fix checkin page when weight is not in the button.
            });
        };
        $http.get('date/' + date + '/activity').success(process);
        // TODO implement .error because it's dangerous when user attempt to save.
    };

    $scope.do_checkin = function(name, weight) {
        if (!_.has($scope.checkins, name)) {
            $scope.checkins[name] = {};
            $scope.checkin_names_list.unshift(name);
        }
        $scope.checkins[name]['weight'] = weight;
        var sum = _.reduce(_.values($scope.checkins), function(sum, c) {return sum + (c['weight'] > 0 ? 1 : 0)}, 0);
        $scope.server_message = "已经点了" + sum + "位会员";
        $scope.checkin_weight_sum = sum;
    }

    $scope.do_deposit = function(name, deposit) {
        if (!_.has($scope.checkins, name)) {
            $scope.checkins[name] = {};
            $scope.checkins[name]['weight'] = 0;
            $scope.checkin_names_list.unshift(name);
        }
        $scope.checkins[name]['deposit'] = deposit;
    }

    $scope.doFilter = function(elem) {
        if (!$scope.info.query) return true;
        return angular.lowercase(elem.index).indexOf(angular.lowercase($scope.info.query)) == 0;
    }
}

function ClubCtrl($scope, $http, $routeParams, $location, $filter, $window) {
    $scope.name = $routeParams.name;
    $scope.info.date = $routeParams.date;
    $scope.deposit = ($scope.checkins[$scope.name] || {})['deposit'];
    console.log("ClubCtrl " + $scope.info.date);

    if ($scope.info.date && $scope.info.date != $scope.info.get_activities_date) {
        $scope.get_activities($scope.info.date);
    }

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
        $location.path('/checkin/' + name);
    }

    $scope.checkin_weight = function(name, weight) {
        $scope.do_checkin(name, weight);
        $window.history.back();
    }

    $scope.checkin_deposit = function(deposit) {
        deposit = Number(deposit);
        if (isNaN(deposit)) return;
        if (deposit < 0) return;
        $scope.do_deposit($scope.name, deposit);
        $window.history.back();
    }

    $scope.isGirl = function(member) {
        if (_.has(member, 'male')) {
            return !member.male;
        }
        var found = _.findWhere($scope.members, {"name": member});
        if (!found) {
            console.log('isGirl member not found: ' + member);
            return false;
        }
        return !found.male;
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
        if ($scope.checkins[$scope.name] && $scope.checkins[$scope.name]['weight'] == w) {
            return 'weight_selected';
        } else {
            return '';
        }
    }
}

function MemberCtrl($scope, $http, $routeParams, $location, $filter, $timeout, $modal) {
    $scope.name = $routeParams.name;

    $scope.edit_member = function(member) {
        var modalInstance = $modal.open({
            templateUrl: 'editModal.html',
            controller: EditModalCtrl,
            resolve: {
                memberEdit: function () {
                    return member;
                }
            }
        });
    }

    $scope.delete_member = function(member) {
        var r = confirm("确定要删除会员“" + member.name + "”吗？");
        var change = {'hidden': true, 'hidden_date': today()};
        if (r == true) {
            $http({
                method: 'PATCH', 
                url: member.resource_uri, 
                data: change,
                headers: {'Content-Type': 'application/json'},
            }).success(function() {
                $scope.members = _.reject($scope.members, function(m) {return m.name == member.name});
                $scope.hidden_members.push(_.extend(member, change));
            });
        }
    }

    $scope.deposit = function(member) {
        $scope.depositEdit = $scope.depositEdit || {};
        $scope.depositEdit["name"] = member.name;
        if (!$scope.depositEdit["date"]) {
            // reuse previous entered date or use default
            $scope.depositEdit["date"] = $scope.info.date;
        }
        $('#depositModal').modal();
    }

    $scope.deposit_save = function() {
        var depositEdit = _.clone($scope.depositEdit);
        deposit = Number(depositEdit["amount"]);
        if (isNaN(deposit) || deposit < 0) {
            alert("输入有误");
            return;
        }

        $scope.info.loading = true;
        var payload = {
            "date": depositEdit["date"],
            "list": [{
                "name": depositEdit["name"],
                "deposit": depositEdit["amount"],
                "weight": 0,
            }]
        }
        $http.post("checkin", payload)
            .success(function(data) {
                if (data != "ok") {
                    alert("保存失败？？");
                    return;
                }
                $('#depositModal').modal('hide');
                // update the member balance in model
                var member = _.findWhere($scope.members, {"name": depositEdit.name});
                member.balance += depositEdit.amount;
                member.balanceStyle = {"background-color": "yellow"};
                $timeout(function() {
                    member.balanceStyle = {};
                }, 1000);
                $scope.info.loading = false;
            });
    }
}

var EditModalCtrl = function ($scope, $modalInstance, $http, memberEdit) {

  $scope.memberEdit = memberEdit;
  
  // Convert dict to an array format
  var extra = JSON.parse(memberEdit.extra);
  $scope.extra = [];
  for (var key in extra) {
    $scope.extra.push({'key': key, 'value': extra[key]});
  }
  $scope.extraOptions = ['手机', 'QQ', '微信', 'Email', '其他'];

  $scope.add_extra = function() {
    $scope.extra.push({'key':'','value':''});
  }

  $scope.del_extra = function(i) {
    $scope.extra.splice(i, 1);
  }

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };

  $scope.edit_member_save = function() {
    var memberEdit = $scope.memberEdit;

    // Convert array format back to dict
    var extra = {};
    for (var i in $scope.extra) {
      var o = $scope.extra[i];
      if (o.key === '') {
        alert('请选择联系方式');
        return;
      }
      if (o.key in extra) {
        alert('请不要选择重复联系方式');
        return;
      }
      extra[o.key] = o.value;
    }
    memberEdit.extra = JSON.stringify(extra);

    $http({
        method: 'PATCH', 
        url: memberEdit.resource_uri, 
        data: memberEdit,
        headers: {'Content-Type': 'application/json'}
    }).success(function () {
        $modalInstance.close(memberEdit);
    }).error(function () {
        alert("出错了，请稍后再试");
    }) ;
  }
};
