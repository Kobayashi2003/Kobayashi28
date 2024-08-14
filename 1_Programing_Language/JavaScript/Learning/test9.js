var points = [40, 100, 1, 5, 25, 10];
points.sort(function(a, b){return a - b});
console.log(points);

var points = [40, 100, 1, 5, 25, 10];
points.sort(function(a, b){return b - a});
console.log(points);
points.reverse();
console.log(points);

function myArrayMax(arr) {
    // return Math.max.apply(null, arr);
    var len = arr.length;
    var max = -Infinity;
    while (len--) {
        if (arr[len] > max) {
            max = arr[len];
        }
    }
    return max;
}

function myArrayMin(arr) {
    // return Math.min.apply(null, arr);
    var len = arr.length;
    var min = Infinity;
    while (len--) {
        if (arr[len] < min) {
            min = arr[len];
        }
    }
    return min;
}

var arr = [1, 2, 3];
var max = myArrayMax(arr);
var min = myArrayMin(arr);

console.log(max);
console.log(min);


var cars = [
    {type:"Volvo", year:2016},
    {type:"Saab", year:2001},
    {type:"BMW", year:2010}
];

cars.sort(function(a, b){return a.year - b.year});
console.log(cars);

cars.sort(function(a, b){
    var x = a.type.toLowerCase();
    var y = b.type.toLowerCase();
    if (x < y) {return -1;}
    if (x > y) {return 1;}
    return 0;
});
console.log(cars);


var txt = "";
var numbers = [45, 4, 9, 16, 25];
numbers.forEach(myFunction);

function myFunction(value, index, array) {
    txt = txt + value + "<br>";
}


var numbers1 = [45, 4, 9, 16, 25];
var numbers2 = numbers1.map(myFunction1);
console.log(numbers2)

function myFunction1(value, index, array) {
    return value * 2;
}


var numbers = [45, 4, 9, 16, 25];
var over18 = numbers.filter(myFunction2);
console.log(over18)

function myFunction2(value, index, array) {
    return value > 18;
}


var numbers = [45, 4, 9, 16, 25];
var sum = numbers.reduce(myFunction3);
console.log(sum)

function myFunction3(total, value, index, array) {
    return total + value;
}


var numbers = [45, 4, 9, 16, 25];
var allOver18 = numbers.every(myFunction4);
console.log(allOver18)

function myFunction4(value, index, array) {
    return value > 18;
}


var numbers = [45, 4, 9, 16, 25];
var someOver18 = numbers.some(myFunction5);
console.log(someOver18)

function myFunction5(value, index, array) {
    return value > 18;
}


var numbers = [45, 4, 9, 16, 25];
var a = numbers.indexOf(16);
console.log(a)


var numbers = [45, 4, 9, 16, 25];
var first = numbers.find(myFunction6);
console.log(first)

function myFunction6(value, index, array) {
    return value > 18;
}


var numbers = [45, 4, 9, 16, 25];
var first = numbers.findIndex(myFunction7);
console.log(first);

function myFunction7(value, index, array) {
    return value > 18;
}

