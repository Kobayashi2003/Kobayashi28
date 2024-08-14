var add = (function () {
    var counter = 0;
    return function () { return counter += 1; }
})();

add();
add();
add();

// 闭包指的是有权访问父作用域的函数，即使在父函数关闭之后。
console.log(add());