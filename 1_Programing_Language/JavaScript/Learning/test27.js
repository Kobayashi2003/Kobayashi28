function Person(first, last, age, eyeColor) {
    this.firstName = first;
    this.lastName = last;
    this.age = age;
    this.eyeColor = eyeColor;
}
Person.prototype.nationality = "English";

Person.prototype.name = function () {
    return this.firstName + " " + this.lastName;
}