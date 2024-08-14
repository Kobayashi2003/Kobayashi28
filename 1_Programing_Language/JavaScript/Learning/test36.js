// 回调是作为参数传递给另一个函数的函数
function myDisplayer(some) {
    console.log(some)
}

function myCalculator(num1, num2, myCallback) {
    let sum = num1 + num2;
    myCallback(sum);
}

myCalculator(5, 5, myDisplayer); // 10

setTimeout(myFunction, 3000); 

function myFunction() {
    console.log("Hello");
}

setInterval(myFunction, 1000); // 每秒钟调用一次函数

function myFunction() {
    let d = new Date();
    console.log(
        d.getHours() + ":" + 
        d.getMinutes() + ":" + 
        d.getSeconds());
}