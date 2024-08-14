//快排前后指针法
function PartSort(left, right) {
    var keyi = left;
    var prev = left;
    var cur = left;
    while(cur <= right) {
        if(arr[cur] < arr[keyi] && ++prev != cur) {
            Swap(cur, prev);
        }
        cur ++;
    }
    Swap(prev,keyi);
    return prev;
}

function Swap(x, y) {
    let tmp = arr[x];
    arr[x] = arr[y];
    arr[y] = tmp;
}

function QuickSort(left, right) {
    if(left >= right) {
        return;
    }
    var keyi = PartSort(left, right);
    QuickSort(left, keyi - 1);
    QuickSort(keyi + 1, right);
}

arr = [5, 3, 2, 4, 1, 10, 9, 8, 7, 6];
QuickSort(0, arr.length - 1);