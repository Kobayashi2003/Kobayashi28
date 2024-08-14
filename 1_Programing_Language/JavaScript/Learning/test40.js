function myDisplayer(some) {
    console.log(some);
}

async function myFunction() {
    return "Hello";
}

myFunction().then(
    function(value) { myDisplayer(value); },
    function(error) { myDisplayer(error); }
);
