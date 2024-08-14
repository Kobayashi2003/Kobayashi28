//斐波那契数列
var tmp1 = 1, tmp2 = 1;
var n = 5;
for(var i = 2; i <= n; i++){
    document.write(tmp1+" ");
    document.write(tmp2+" ");
    tmp1 = tmp1 + tmp2;
    tmp2 = tmp1 + tmp2;
}