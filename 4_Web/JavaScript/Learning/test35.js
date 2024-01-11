class Car {
    constructor(brand) {
        this.carname = brand;
    }
    present() {
        return 'I have a ' + this.carname;
    }
    get cnam() {
        return this.carname;
    }
    set cname(x) {
        this.carname = x;
    }
    static hello() {
        return 'Hello!!';
    }
}

class Model extends Car {
    constructor(brand, mod) {
        super(brand);
        this.model = mod;
    }
    show() {
        return this.present() + ', it is a ' + this.model;
    }
}

let myCar = new Model('Ford', 'Mustang');
console.log(myCar.show());
console.log(myCar.cnam);
console.log(Car.hello());