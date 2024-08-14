function Person(first, last, age, eye) {
    // in the constructor function, this does not have a value.
    // this refers to the new object being created by the constructor.
    this.firstName = first;
    this.lastName = last;
    this.age = age;
    this.eyeColor = eye;
    this.nationality = "English";
    this.name = function () {
        return this.firstName + " " + this.lastName;
    }
}


var myFather = new Person("John", "Doe", 50, "blue");
var myMother = new Person("Sally", "Rally", 48, "green");

myFather.name = function () {
    return this.firstName + " " + this.lastName;
} 

