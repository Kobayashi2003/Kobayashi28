(function () {
    console.log('Hello!!')
})();

function myFunction() {
    return arguments.length; 
}

console.log(myFunction(1, 2, 3, 4, 5, 6, 7, 8, 9, 10));

console.log(myFunction.toString());