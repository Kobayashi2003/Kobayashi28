function findMax() {
    var i;
    var max = -Infinity;
    for (i = 0; i < arguments.length; i++) {
        if (arguments[i] > max) {
            max = arguments[i];
        }
    }
    return max;
}

var max = findMax(1, 123, 500, 115, 44, 88);
console.log(max);


function sumAll() {
    var i, sum = 0;
    for (i = 0; i < arguments.length; i++) {
        sum += arguments[i];
    }
    return sum;
}

var sum = sumAll(1, 123, 500, 115, 44, 88);
console.log(sum);
