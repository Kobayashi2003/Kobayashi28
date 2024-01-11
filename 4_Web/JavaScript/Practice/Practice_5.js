// 将任意进制转换为任意进制(2-36)
// 输入数据
var number = window.prompt('Input');
// 输入基底进制
var radix1 = parseInt(window.prompt('Input'));
// 输入目标进制
var radix2 = parseInt(window.prompt('Input'));
// 将输入数从基底进制转换为目标进制
console.log(parseInt(number,radix1).toString(radix2));