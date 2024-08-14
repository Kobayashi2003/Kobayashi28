const person = {
    firstName: "Bill",
    lastName: "Gates",
    fullName: function () {
        return this.firstName + " " + this.lastName;
    }
}

const member = {
    firstName: "Hege",
    lastName: "Nilsen",
}

let fullName = person.fullName.call(member);
console.log(fullName); // Hege Nilsen

let fullName2 = person.fullName.apply(member);
console.log(fullName2); // Hege Nilsen

let fullName3 = person.fullName.bind(member);
console.log(fullName3);
