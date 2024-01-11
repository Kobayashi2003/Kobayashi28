// Hoisting

// use strict

"use strict";

// JavaScript this keyword
    // in a method, this refers to the owner object
    // alone, this refers to the global object
    // in a function, this refers to the global object
    // in a function, in strict mode, this is undefined
    // in an event, this refers to the element that received the event
// methods like call(), and apply() can refer this to any object

var person1 = {
    fullName: function() {
        return this.firstName + " " + this.lastName;
    }
}

var person2 = {
    firstName: "John",
    lastName: "Doe",
}

console.log(person1.fullName.call(person2));