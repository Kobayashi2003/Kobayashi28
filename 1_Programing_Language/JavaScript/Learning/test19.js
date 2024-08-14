// 箭头函数 (Arrow Function)

let myFunction = (a, b) => a * b;
console.log(myFunction(2, 3)); // 6

hello = () => {
    return "Hello World!";
}
console.log(hello());

hello1 = () => "Hello World!";
console.log(hello1());

hello2 = (val) => "Hello " + val;
console.log(hello2("World!"));

hello3 = val => "Hello " + val;
console.log(hello3("World!"));

// 对于箭头函数，this 关键字始终表示定义箭头函数的对象。