async function myDisplay() {
    let myPromise = new Promise(function(myResolve, myReject) {
        // myResolve("I love You !!");
        setTimeout(function() {
            myResolve("I love You !!");
        }, 3000);
    });
    let result = await myPromise;
    console.log(result);
}

myDisplay();