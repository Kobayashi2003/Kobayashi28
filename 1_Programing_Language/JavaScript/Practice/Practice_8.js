// 阶乘
var n = window.prompt('Input');
function factorial(n){
    return n == 0 ? 1 : n * factorial(n - 1);
}
console.log(factorial(n))
;