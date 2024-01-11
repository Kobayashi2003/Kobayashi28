// 实现在原型链上的递归式快速排序
// 完成于2022/6/15
// 注意： 1、在立即执行函数中，this的指向会默认指向全局，即window（es3.0）
//       2、注意谁调用的函数，this就指向谁，因此在递归的时候this值会随着递归的进行不断变化，若只希望保持第一次的this的值，最好使用变量将其保存
var arr =  [3,5,2,4,7];
Array.prototype.quickSort = function (Low, High, Arr) {
    Low = (Low == undefined) ? 0 : Low;
    High = (High == undefined) ? this.length - 1 : High;
    Arr = (Arr == undefined) ? this : Arr;
    var middle = (function (low, high) {
        var partElement = Arr[low];
        while(true) {
            while(low < high && partElement <= Arr[high]) {
                high--;
            }
            if(low >= high) {
                break;
            }
            Arr[low++] = Arr[high];
            while(low < high && Arr[low] <= partElement) {
                low++;
            }
            if(low >= high) {
                break;
            }
            Arr[high--] = Arr[low];
        }
        Arr[high] = partElement;
        return high;
    }(Low, High));
    if(Low < High) {
        Array.prototype.quickSort(Low, middle - 1, Arr);
        Array.prototype.quickSort(middle + 1, High, Arr);
    }
}