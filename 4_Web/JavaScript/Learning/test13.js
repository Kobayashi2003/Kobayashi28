var person = {
    fname: "John",
    lname: "Doe",
    age: 25
};

for (x in person) {
    console.log(x + ": " + person[x])
}


const numbers = [45, 4, 9, 16, 25];

let txt = "";
numbers.forEach(myFunction);
console.log(txt);

function myFunction(value, index, array) {
    txt += value;
}


const cars = ["BMW", "Volvo", "Saab", "Ford"];

let text = "";
for (let x of cars) {
    text += x + " ";
}
console.log(text);


