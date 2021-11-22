
var app = angular.module('myApp', []);
app.controller('myCtrl',['$scope','$http','$timeout', function($scope,$http,$timeout) {
    $scope.vm = {};
    $scope.vm.not_allow_download = true;
    $scope.vm.formula_show = false;
    $scope.vm.loaded_formula = {}
//    $scope.$watch("vm.formula",function(newValue,oldValue){
//        //adding some chars
//        if(newValue.length > oldValue.length) {
//            var value = newValue.replace(oldValue,'').replace(/\s+/,'');
//            if(value.match(/[a-zA-Z]/)) {
//                $scope.vm.params[value] = 0;
//                console.log(value)
//            }
//        }else {
//        //deleting some chars
//            var value = oldValue.replace(newValue,'').replace(/\s+/,'');
//            if(value.match(/[a-zA-Z]/)) {
//                if($scope.vm.params.hasOwnProperty(value)) {
//                    delete $scope.vm.params[value];
//                }
//                console.log('delete: ' + value)
//            }
//        }
//        console.log($scope.vm.params)
//    });

    $scope.vm.submit = function() {
        if(!$scope.vm.formulas) {
            $scope.vm.raiseError('请选择题目模版！')
            return
        }
        if(!$scope.vm.formulaNumbers) {
            $scope.vm.raiseError("请填写生成题目数量")
            return
        }
        angular.forEach($scope.vm.formulaNumbers ,function(number){
            if ((!number) || (parseInt(number) <= 0)) {
                $scope.vm.raiseError("请填写生成题目数量")
                return
            }
        });
        $scope.vm.preview = false;
        $scope.vm.result = []
        var data = []
        count = 0
        angular.forEach($scope.vm.formulas ,function(f){
            data.push({'model': f, 'number': $scope.vm.formulaNumbers[count]})
            count = count + 1;
        });
        console.log(data)
        $http({
                url: "/generateFormula",
                method: "POST",
                data: {'data': data}
                }).then(function (output) {
                    if(output.status !== 200) {
                        $scope.vm.raiseError("生成题目失败！")
                    }else {
                        $scope.vm.preview = true;
                        var temp = []
                        angular.forEach(output.data.data.split('@') ,function(data,index,objs){
                            temp.push(data);
                            if ((index + 1) % 5 ==0) {
                                $scope.vm.result.push(temp);
                                temp = []
                            }
                        });
                        if (temp.length != 0) {
                            $scope.vm.result.push(temp);
                        }
                        $scope.vm.not_allow_download = false;
                    }
                }).catch(function(output, status) {
                    $scope.vm.raiseError("500 服务器内部错误！")
            });
    }

    $scope.vm.download = function() {
        $http({
                url: "/downloadFormula",
                method: "POST",
                data: {'data': JSON.stringify($scope.vm.result)},
                responseType: 'arraybuffer'
                }).then(function (output) {
                    if(output.status !== 200) {
                        alert("fail!")
                    }else {
                         console.log('success')
                        var blob = new Blob([output.data], {type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"});
                        var objectUrl = URL.createObjectURL(blob);
                        var aForExcel = $("<a><span class='forExcel'>download</span></a>").attr("href",objectUrl);
                        $("body").append(aForExcel);
                        $(".forExcel").click();
                        aForExcel.remove();
                    }
                });
    }

    $scope.vm.raiseError = function(msg) {
        $scope.vm.errorMessage = msg;
        $scope.vm.error_show = true;
        $timeout(function(){
            $scope.vm.error_show = false;
         },5000);
    }

}]);
