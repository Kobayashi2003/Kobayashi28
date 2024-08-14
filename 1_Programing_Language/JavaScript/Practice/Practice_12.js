//快排挖坑法
function PartSort(left, right) {
    var key = arr[left];
    var hole = left;//挖坑
    while(left < right) {
        while(left < right && arr[right] >= key) {
            right --;
        }
        arr[hole] = arr[right];//填坑
        hole = right;//挖新坑
        while(left < right && arr[left] <= key) {
            left ++;
        }
        arr[hole] = arr[left];
        hole = left;
    }
    arr[hole] = key;
    return hole;
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