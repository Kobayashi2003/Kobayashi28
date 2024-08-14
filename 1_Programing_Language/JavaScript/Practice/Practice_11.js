// hoare快排
function PartSort(left, right) {
    var key = right;
    while(left < right) {
        while(left < right && arr[left] <= arr[key]) {
            left ++;
        }
        while(left < right && arr[right] >= arr[key]) {
            right --;
        }
        Swap(left, right);
    }
    Swap(left, key);
    return left;
}

function QuickSort(left, right) {
    if(left >= right) {
        return;
    }
    var keyi = PartSort(left, right);
    QuickSort(left, keyi - 1);
    QuickSort(keyi + 1, right);
}

function Swap(left, right) {
    let tmp = arr[left];
    arr[left] = arr[right];
    arr[right] = tmp;
}

arr = [5, 3, 2, 4, 1, 10, 9, 8, 7, 6];
QuickSort(0, arr.length - 1);