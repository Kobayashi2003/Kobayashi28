function isArray(myFunction) {
    return myFunction.constructor.toString().indexOf("Array") > -1; 
}

const myArr = [1, 2, 3, 4, 5];
console.log(isArray(myArr));


function isArray2(myFunction) {
    return myFunction.constructor === Array;
}

const myArr2 = [1, 2, 3, 4, 5];
console.log(isArray2(myArr2));