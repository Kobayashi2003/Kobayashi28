// 输入一串字符，并写一个函数将他们反转进行输出
var string = window.prompt('Input');
function reverse(string){
    var tmp = "";
    for(var i = string.length - 1; i >= 0; i--){
        tmp += string[i];
    }
    return tmp;
}
console.log(reverse(string));