function MemberListCtrl($scope, $http) {
    $http.get('api/member/?format=json').success(function(data) {
        $scope.members = data.objects;
    });

    $scope.doFilter = function(elem) {
        if (!$scope.query) return true;
        return angular.lowercase(elem.index).indexOf(angular.lowercase($scope.query)) == 0;
    }
}
