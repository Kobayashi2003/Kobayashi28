const cars = ["Saab", "Volvo", "BMW"];
// 用 const 声明的数组不能重新赋值：
// cars = ["Toyota", "Volvo", "Audi"];    // 错误

// 数组不是常量
// 关键字 const 有一定误导性
// 它不定义常量数组，它定义的是对数组的常量引用
// 因此。我们仍然可以更改常量数组的元素


cars[0] = "Toyota";
console.log(cars);

cars.push("Audi");
console.log(cars);
