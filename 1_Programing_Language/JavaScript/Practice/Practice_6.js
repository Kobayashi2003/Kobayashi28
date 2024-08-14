// soap sort
var arr = [1,2,3,4,5,6,7,8,9,10];
for(var i = 0; i < arr.length; i++) {
    for(var j = i + 1; j < arr.length; j++) {
        if(arr[i] < arr[j]){
            var tmp = arr[i];
            arr[i] = arr[j];
            arr[j] = tmp;
        }
    }
}
for(var i = 0; i < arr.length; i++){
    console.log(arr[i]);
}