function Init(data) {
    var preData = 'Goodbye World!';
    this.data = data;
    this.changeData = function () {
        this.data = preData;
    }
    this.showData = function () {
        console.log(this.data);
    }
    this.showPredata = function () {
        console.log(preData);
    }
    this.changeData = function () {
        this.data = preData;
    }
    this.changePredata = function (newData) {
        preData = newData;
    }
}

var init = new Init('Hello World!');
init.showData();
init.showPredata();
init.changeData();
init.showData();
init.changePredata('Hello World!!!');
init.showPredata();
init.changeData();
init.showData();