myNumbers = {};

myNumbers[Symbol.iterator] = function () {
    let n = 0;
    let done = false;
    return {
        next() {
            n += 10;
            if (n > 100) {
                done = true;
            }
            return { value: n, done: done };
        }
    };
}

for (const num of myNumbers) {
    console.log(num);
}

let iterator = myNumbers[Symbol.iterator]();
while (true) {
    let result = iterator.next();
    if (result.done) {
        break;
    }
    console.log(result.value);
}