// 将一串英文字母依照ASCII转换为二进制数并输出
var str = '\2'
for(var i = 0; i < str.length; i++) {
    console.log(str[i].charCodeAt().toString(2));
}