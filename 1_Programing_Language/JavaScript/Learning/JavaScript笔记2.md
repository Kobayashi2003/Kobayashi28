# JavaScript笔记2

[toc]

## 继承

### 继承发展史

1. 传统形式 --> 原型链
> 过多的继承了没用的属性

```JS
// 实现例
Father.prototype = {
    lastName : 'Lin',
    Work : 'Officer'
}
var father = new Father();
Son.prototype = father;
function Son = {
    school : '大山中学'
}
var son = new Son();
```

2. 借用构造函数
> 不能继承借用构造函数的原型
> 每次构造函数都要多走一个函数

```JS
// 实现例
function Design(color, width, height) {
    this.color = color;
    this.width = width;
    this.height = height;
}
function Car(color, width, height, brand) {
    Design.call(this, color, width, height);
    this.brand = brand;
}
var car = new Car();
```

3. 共享原型
> 不能随便改动自己的原型

```JS
// 实现例
Father.prototype.lastName = 'Lin';
function Father() {
}
function Son() {
}
Son.prototype = Father.prototype; // 共有原型
var father = new Father();
var son = new Son();
```

4. 圣杯模式

```JS
// 实现例
Father.prototype.lastName = 'Lin';
function Father() {
}
function F() {}
F.prototype = Father.prototype; // F()充当一个中间层
Son.prototype = new F();
```

```JS
function inherit(Target, Origin) {
    function F() {
        F.prototype = Origin.prototype;
        Target.prototype = new F();
        Target.prototype.constructor = Target; // 修复指向紊乱
        Target.prototype.uber = Origin.prototype; // 保留真实继承来源
    }
    Father.prototype.lastName = "Lin";
    function Father() {
    }
    function Son() {
    }

    inherit(Son, Father);
    var son = new Son();
    var Father = new Father();
}
```

```JS
var inherit = (function() {
    var F = function() {}; // 将 F() 写为了私有化变量
    return function (Target, Origin) {
        F.prototype = Origin.prototype;
        Target.prototype = new F();
        Target.prototype.constructor = Target;
        Target.prototype.uber = Origin.prototype;
    }
});
```

## 命名空间

管理变量,防止污染全局,适用于模块化开发

```JS
// 老办法:命名空间 --> 实质就是对象
var holo_EN = {
    EN_season1 : {
        member1 : 'Garw Grua',
        member2 : 'Watson Amelia',
        member3 : "Ninomae Ina'nis",
        member4 : 'Takanashi Kiara',
        member5 : 'Mori Calliope'
    },
    EN_season2 : {
        member1 : 'Tsukumo Sana',
        member2 : 'Ceres Fauna',
        member3 : 'Ouro Kronii',
        member4 : 'Nanashi Mumei',
        menber5 : 'Hakos Baelz'
    }
}
var member = holo_EN.EN_season1;
```

```JS
// 可以通过使用闭包实现私有化以防止全域内互相污染
var name = 'bcd';
var init = (function () {
    var name = 'abc'

    function callName() {
        console.log(name);
    }

    return function () {
        callName();
    }
})
init(); // 'abc'
```

## 对象的枚举

枚举 enum（enumeration）

```JS
var obj = {
    elm1 : 'test1',
    elm2 : 'test2',
    elm3 : 'test3',
    __proto__ : {
        elem4 : 'test4'
    }
}
for(var prop in obj) { // for-in 循环，用于遍历对象，对象中有多少的属性就会循环多少次，每次循环系统都会用对象中的一个属性的名字来替代 prop

// 属性 in 对象 能够判断一个对象能不能访问到该属性

    console.log(prop); // prop 的类型为 String，打印出的为对象中的属性名

    console.log(obj.prop); // 输出均为 undefined
    // 底层原则：因为系统会隐式将 obj.prop ----> obj['prop'] （系统将会认为你想要访问 obj 中的 prop 属性）

    // 正确写法
    console.log(obj[prop]); // test1 test2 test3 test4
    // prop 能够沿着原型链向上访问 （系统自设的会自动忽略）

    if(obj.hasOwnProperty(prop)) { // hasOwnProperty() 判断该 prop 所代表的属性是否为对象本身的属性，调用后返回一个布尔值
        console.log(obj[prop]); // test1 test2 test3
    }
}
```

### instanceof

```JS
function Person() {

}

var person = new Person();

console.log(person instanceof Person); // true

// A instanceof B
// 判断 A 对象的原型链上有没有 B 的原型
```

应用：判断一个变量是 数组 还是 对象

1. 方法一：通过 constructor属性 进行判断
```JS
var array = [];
var obj = {};
console.log(array.constructor); // Array()
console.log(obj.constructor); // Object()
```
2. 方法二：通过 instanceof 进行判断
```JS
var array = [];
var obj = {};
console.log(array instanceof Array); // true
console.log(obj instanceof Array); // false
```
3. 方法三:
```JS
var array = [];
var obj = {};
console.log(Object.prototype.toString.call(array)); //[object Array]
console.log(Object.prototype.toString.call(obj)); // [object Object]
// toString 识别的是 this，通过 call 能够改变 this 的指向
// 也可以通过这一方法识别其它的变量类型
```

## arguments克隆

```JS
// 深度克隆

var obj = {
    name : 'a',
    age : 123,
    card : ['visa', 'master'],
    wife : {
        name : 'b',
        son : {
            name : 'c'
        }
    }
}

// 遍历对象 for(var prop in obj)
// 1.判断是不是原始值   typeof()
// 2.判断是数组还是对象 instanceof toString（推荐） construtor
// 3.建立相应的数组或对象
// 递归

function deepClone(origin, target) {

    var target = target || {},
        toStr = Object.prototype.toString,
        arrStr = '[object Array]';

    for(var prop in origin) {
        if(origin.hasOwnProperty(prop)) {

            if(obj[prop] !== 'null' && typeof(origin[prop]) == 'object') {

                if(toStr.call(origin[prop]) == arrStr) {
                    target[prop] = [];
                }
                else {
                    target[prop] = {};
                }

                deepClone(origin[prop], target[prop]);
            }
            else {
                target[prop] = origin[prop];
            }
        }
    }

    return target;
}

var newObj = deepClone(obj);

```

## 三目运算符

条件判断? 是 : 否 并且会返回值

## 数组

### 数组的定义

```JS
var arr1 = [1,2,3];
// 写有多余的逗号不会报错，缺少的元素将会表示为 undefined （这类数组被称为稀松数组）
var arr2 = new Array(1,2,3,4,5);
// 若用第二种方法构造，并且 Array() 中只有一个 Number 参量，则该参量将会默认为该数组的长度（length）
```

### 数组的读和写

JS中的数组会自动扩充，不会溢出
<!-- 数组就是一种特殊的对象 -->

### 数组常用的方法

#### 改变原数组

##### push

```JS
var array = [];
arr.push(10); // 10
arr.push(2); // 10,2
arr.push(1,2,3); // 10,2,1,2,3
// 在数组后增添东西
```

```JS
// 自己写个 push
var arr = [];
Array.prototype.myPush = function () {
    for(var i = 0; i < arguments.length; i++) {
        this[this.length] = arguments[i];
    }
    return this.length;
}
```

##### pop

```JS
var arr = [1,2,3];
arr.pop(); // 将数组的最后一位剪切出来 3 arr --> [1,2]
```

##### unshift

在数组前添加东西（与 push 方向相反）

##### reverse

```JS
var arr = [1,2,3];
arr.reverse(); // 将数组中元素的顺序逆反 arr --> [3,2,1]
```

##### splice

```JS
var arr = [1,1,2,2,3,3];
// 从第几位开始，截取多少长度，在切口处添加的新数据，并且返回截取的部分
// arr.splce(0,3); // [1,1,2]  arr --> [2,3,3]
arr.splice(1,1,0,0,0); // arr --> [1,0,0,0,2,2,3,3]

var arr1 = [1,2,3,5];
arr.splice(3,0,4) // arr1 --> [1,2,3,4,5]
arr.splice(-1,1) // 5 arr1 --> [1,2,3,4]

// splice = function (pos) {
//     pos += pos > 0 ? 0 : this.length; // 数组中负数位的处理方法
// }
```

##### sort

```JS
var arr = [1,2,6,3,5,4]
arr.sort(); // arr --> [1,2,3,4,5,6]
var arr1 = [1,2,10,4]
arr1.sort(); // arr1 --> [1,10,2,4] 说明 sort方法 是按照字符串的大小进行排序的


// sort 方法中自带一个方法接口
// 1.必须写两个形参
// 2. 看返回值 1) 当返回值为负数时，那么前面的数放在前面
//            2) 为正数，那么后面的数在前面
//            3) 为 0 ，不动
arr1.sort(function (a, b) {// a,b 为数组内的两个元素，传参顺序符合冒泡排序
    // if(a > b) {
    //     return 1;
    // }else {
    //     return -1;
    // }
    return a - b; // 升序
    // return b - a; // 降序
});// 该函数将会直接执行
```

```JS

// 给一个有序的数组，要求实现该数组的乱序
// Math.random() 提供一个介于 0 与 1 之间的随机数

var arr = [1,2,3,4,5];

arr.sort(function () {
    return Math.random - 0.5;
});

```

```JS
// 功能拓展
var obj1 = {
    num : 10
};
var obj2 = {
    num : 2
};
var obj3 = {
    num : 5
};
var arr = [obj1,obj2,obj3];
arr.sort(function (a,b) {
    return a.num - b.num;
});
```

#### 不改变原数组

##### concat

```JS
var arr1 = [1,2,3];
var arr2 = [4,5,6];
arr1.concat(arr2); // [1,2,3,4,5,6] 返回连接后的数组，但不会改变原数组
```
##### toString

<!-- blank -->

##### slice

```JS
var arr = [1,2,3,4];
var newArr = arr.slice(1,2); // [2] 从哪位开始截取，截取到哪为，返回截取后的数组，且不改变原数组
// 不写参数默认截取整个数组
```

##### join

```JS
var arr = [1,2,3];
arr.join('-')// '1-2-3' 用参数将数组的每一个元素连接成为一个字符串，不写参数时默认使用 ',' 进行连接
```

##### split

```JS
var str = '1-2-3';
str.split('-'); // ['1','2','3'] 按照一定规则将一个字符串拆分为一个数组（split 为字符串方法）
```

##### 数组去重

```JS
var arr = [1,1,2,2,'a','a'];

Array.prototype.unique = function () {
    var hashTable = {};
    var arr = [];
    var len = this.length;
    for(var i = 0; i < len; i++) {
        if(!hashTable[this[i]]) {
            hashTable[this[i]] = "Exist";
            arr.push(this[i]);
        }
    }
    return arr;
}
```


## 类数组

```JS
// 类数组格式
// 属性要为索引（数字）属性，必须要有length属性，最好加上push
// 类数组仍为一个对象

var obj = {
    "0" : 'a',
    "1" : 'b',
    "2" : 'c',
    "length" : 3,
    "push" : Array.prototype.push
};

obj.push('d');
// obj -->
// var obj = {
//     "0" : 'a',
//     "1" : 'b',
//     "2" : 'c',
//     "3" : 'd',
//     "length" : 4,
//     "push" : Array.prototype.push
// };
```

```JS
// 例题
var obj = {
    "2" : 'a',
    "3" : 'b',
    "length" : 2,
    "push" : Array.prototype.push
};
obj.push('c');
obj.push('d');

// 答案
// obj = {
//     "2" : 'c',
//     "3" : 'd',
//     "length" : 4,
//     "push" : Array.prototype.push
// }
```

### 类数组的优点

同时具有了数组与对象的特点（但不是具备数组的全部特点，但是可以自行添加）


## try catch

```JS
// 在 try 中的语句若出现错误，则系统仍会报错，但系统将不会抛出错误
// 在 try 里面的语句发生错误，不会执行错误语句后并且包含在try 语句中的代码，但在 try 语句后的代码仍能够继续执行
try {
    console.log('a');
    console.log(b); // 出现错误
    console.log('c') // 错误语句后的语句将停止执行
}catch(e) { // error对象 error.message（错误信息） error.name（错误名称） --> error
    console.log(e.message + " " + e.name); // 若 try 语句中出现错误，系统将会执行 catch 中的语句
}
console.log('d'); // 仍继续执行
```

## Error.name的六种值对应的信息

1. EvalError: eval()的使用与定义不一致
2. RangeError: 数值越界
3. ReferenceError: 非法或不能识别的引用数值
4. SyntaxError: 发生语法解析错误
5. TypeError: 操作类型错误
6. URIError: URI处理函数使用不当

## es5严格模式

> 在启用es5.0严格模式时，es3.0和es5.0产生冲突的部分将采用es5.0方法解决，否则将采用es3.0的方法

```JS
"use strict"; // es5.0严格模式的启动（严格模式可通过这串字符串启用，这种启用方式的好处在于不会对不兼容严格模式的浏览器产生影响）

// 不再兼容es3的一些不规则语法（例如 with模块,callee函数等将无法使用），使用全新es5语法
// 两种用法：
    // 1）全局严格模式
    // 2）局部函数内严格模式

// 新规则：不支持 with，arguments.callee，func，caller
// 变量赋值前必须声明
// 局部变量 this 必须被赋值（Person.call(null/undefined)赋值什么就是什么,直接传原始值系统将不会再将其变化为包装类再赋值给 this）
// 拒绝重复参数和属性



// eval() 能够将字符串作为代码执行 es3.0无法使用
// with(obj){}模块 能够将模块内的 AO 首位更换为括号内的 Obj es5.0无法使用
```