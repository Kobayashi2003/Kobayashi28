var number1 = parseInt(window.prompt('Input'));
var number2 = parseInt(window.prompt('Input'));
// 随意输入两个数，分别输出两个数的最小公倍数与最大公约数
//最小公倍数
var i = 0;
for(i = number1 > number2 ? number1 : number2; i < number1 * number2; i++){
    if(i % number1 == 0 && i % number2 == 0){
        break;
    }
}
document.write("最小公倍数为：" + i + "</br>");
for(i = number1 < number2 ? number1 : number2;/*blank*/; i--){
    if( number1 % i == 0 && number2 % i == 0){
        break;
    }
}
document.write("最大公约数为：" + i + "</br>");