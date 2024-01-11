function quickSort(low,high) {
    //打印数组
    for(let k = 0; k < arr.length; k++) {
        document.write(arr[k] + " ");
    }
    document.write("</br>");

    var middle;
    if(low >= high) {//当序号low大于等于序号high时说明排序已完成，结束函数
        return;
    }
    middle = spilt(low,high);
    quickSort(low,middle -1);
    quickSort(middle + 1,high);
}

function spilt(low,high) {
    var partElement = arr[low];
    while(1)
    {
        while(low < high && partElement <= arr[high]) {
            high --;
        }
        if(low >= high) {
            break;
        }
        arr[low++] = arr[high];

        while(low < high && arr[low] <= partElement) {
            low ++;
        }
        if(low >=high) {
            break;
        }
        arr[high--] = arr[low];
    }
    arr[high] = partElement;
    return high;
}

var arr = [10,7,8,5,4,2,1,0,11,3];
quickSort(0,arr.length - 1);