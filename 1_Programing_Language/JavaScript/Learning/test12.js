console.log(Math.PI);

console.log(Math.round(4.7));
console.log(Math.round(4.4));

console.log(Math.pow(8, 2));

console.log(Math.sqrt(64));

console.log(Math.abs(-4.7));

console.log(Math.ceil(4.4));
console.log(Math.ceil(4.7));

console.log(Math.floor(4.4));
console.log(Math.floor(4.7));

console.log(Math.sin(90 * Math.PI / 180));
console.log(Math.cos(0 * Math.PI / 180));

console.log(Math.min(0, 150, 30, 20, -8, -200));
console.log(Math.max(0, 150, 30, 20, -8, -200));

console.log(Math.random()); 

function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min) ) + min;
}

function getRndInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1) ) + min;
}