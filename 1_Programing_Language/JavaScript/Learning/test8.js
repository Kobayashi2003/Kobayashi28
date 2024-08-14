let x = 9.656;
console.log(x.toExponential(2));
console.log(x.toExponential(4));

console.log(x.toFixed(0));
console.log(x.toFixed(2));
console.log(x.toFixed(4));
console.log(x.toFixed(6));

console.log(x.toPrecision());
console.log(x.toPrecision(2));
console.log(x.toPrecision(4));
console.log(x.toPrecision(6));

console.log(Number(true));
console.log(Number(false));
console.log(Number("10"));
console.log(Number("  10"));
console.log(Number("10  "));
console.log(Number(" 10  "));
console.log(Number("10.33"));
console.log(Number("10,33"));
console.log(Number("10 33"));
console.log(Number("Bill"));


console.log(parseInt("-10"));
console.log(parseInt("-10.33"));
console.log(parseInt("10"));
console.log(parseInt("10.33"));
console.log(parseInt("10 20 30"));
console.log(parseInt("10 years"));
console.log(parseInt("years 10"));


console.log(parseFloat("10"));
console.log(parseFloat("10.33"));
console.log(parseFloat("10 20 30"));
console.log(parseFloat("10 years"));
console.log(parseFloat("years 10"));


console.log(Number.EPSILON);

function isArray(x) {
    return x.constructor.toString().indexOf("Array") > -1;
}

arr = [];
console.log(isArray(arr));
console.log(arr instanceof Array);

for(let i = 0; i < 10; ++i) 
    arr.push(i);

arr;
console.log(arr.shift());
console.log(arr.shift());
console.log(arr.pop());
console.log(arr.unshift(10));
arr;


