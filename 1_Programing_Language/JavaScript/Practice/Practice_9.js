// 写一个方法，求一个字符串的字节长度（提示： 字符串有一个方法charCodeAt();一个中文占两个字节，一个英文占一个字节）

// 定义和用法
// charCodeAt()方法可返回指定位置的字符的Unicode的代码。这个返回值是65535之间的整数。（当返回值为<=255时，为英文，当返回值大于255时为中文）

// 语法
// stringObject.charCodeAt(index)

// eg:
// <script type="text/javascript">
//     var str = "Hello World!";
//     document.write(str.charCodeAt(1));//输出101
// </script>

function countByte(string) {
    var count = 0;
    for(var i = 0; i < string.length; i++) {
        switch(string.charCodeAt(i) <= 255) {
            case true :
                count += 1;
                break;
            case false :
                count += 2;
                break;
        }
    }
    console.log(count);
}
var string = window.prompt("Input");
countByte(string);