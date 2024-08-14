//闭包练习 储存器
function memory() {
    var DATA = "";
    var obj = {
        push : function (data) {
            DATA += data;
        },
        pop : function () {
            console.log(DATA);
        },
        refresh : function () {
            DATA = "";
        }
    };
    return obj;
}

var fun = memory();