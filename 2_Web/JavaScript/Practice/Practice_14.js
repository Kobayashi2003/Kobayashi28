//闭包练习 累加器
function counter() {
    var count = 0;
    function closure() {
        count ++;
        return count;
    }
    return closure;
}

var fun = counter();
var cont = fun();//每执行一次，fun()返回的值便会加 1