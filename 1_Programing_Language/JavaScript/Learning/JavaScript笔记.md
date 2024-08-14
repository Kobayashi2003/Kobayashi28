# JavaScript

[toc]

<!-- es3.0 es5.0 es6.0 -->

<!-- 结构(html) 行为(js) 样式(css) 相分离 -->

## 主流浏览器与其内核
IE      trident
Chrome  webkit/blink
firefox Gecko
Opera   presto
Safari  webkit


## JavaScript的特点
oka语言 java

主要特点1、JavaScript **解释性语言** （翻译一行执行一行）
<!-- 优点：跨平台 缺点：速度较慢 -->

主要特点2、JavaScript （的引擎）是**单线程**的

```html
何为单线程与多线程：

    单线程 同一时间只能干一件事（同步执行）
                                            （计算机术语里面的描述跟现实生活的是反过来的 就是这么吊诡）
    多线程 同时能干多件事（异步执行）
```

<!--
JavaScript为**动态语言**

ECMA标准：JavaScript兼容ECMA标准，因此也称为ECMAScript

但现在的JavaScript包括了ECMA DOM（文档处理） BOM
-->

## JS的执行队列
**轮转时间片**：将多个任务切割为极小段，争抢时间片段（其最终结果完全随机）之后排成一列执行



## JavaScript基本语法

### 变量

1. **变量声明**
    声明、赋值分解
    单一 var（声明变量的关键字只有一个）

2. **命名规则**
    类似C语言

3. **值类型**

    a. **原始值**(存放在stack)
        1). Number（浮点型）：数字类型
        2). Boolean：布尔类型
        3). String：字符串类型
        4). Undefined：未定义
        5). Null


    b. **引用值**(大致存放在heap)
        1). Array
        2). Object
        3). Function
        ...date RegExp

### 语法基本规则
    1. 语句后面要用分号结束
    2. js语法错误会引发后续代码终止，但不会影响其它js代码块

### 运算操作符
    "+"
        1、数学运算、字符串连接
        2、任何数据类型加字符串都等于字符串
    ……


### 一些JS内的特殊运算
0/0 ->NaN -> Not a number
1/0 ->Infinity Number


<!--
编程形式的区别
1、面向过程
2、面向对象
-->

## typeof
number string boolean object(对象、数组、null都会返回为obiect) undefined function

> typeof()的返回值为**String**类型

## 类型转换

### 显式类型转换
例如：
1). Number('123')
> 对于明显不是数字的数据只能转换成NaN

2). parseInt(demo,redix) ->（以目标进制为基底转换为十进制）
> 转换为整型数,redix表示以什么进制为基底（redix的取值范围2-36）
<!-- parseInt会从第一位开始看看到第一个非数字位置为止 -->

3). parseFloat(string)（同理）

4). 转换为字符串
写法一：toString（undefined、NaN都不能用toString方法）
<!-- 因为undefined与NaN都无法生成包装类，因此无法通过原型链向上查找到toString方法 -->

<!-- document.write()方法会隐式调用toString,因此document.write(obj)就相当于document.write(obj.toString()) -->

写法二：demo.toString()
```JS
var num = 123;
num.toString();// --> new Number(num).toString;
```

> toString(radix) （以十进制为基底将所选数据转换为目标进制）

### 隐式类型转换

例如：
1). isNaN()
> 先将内部数据放入Number()后再去判断是否为NaN

2).
```JS
a="123";
a++;// 先将a转换为数字之后再++
```
3).
```JS
undefined == null
NaN != NaN
```

……

例题：
```JS
    var str = false + 1;
    document.write(str);
    var demo = false == 1;
    document.write(demo);
    if(typeof(a) && -true + (+undefined) + ""){
        document.write('TEST1');
    }
    if(11 + "11" * 2 == 33){
        document.write('TEXT2');
    }
    !!" " + !!"" - !!false||document.write('TEXT3');
```

答案：
```JS
    var str = false + 1;
    document.write(str);//1
    var demo = false == 1;
    document.write(demo);//false
    if(typeof(a)/*undefined（这是字符串）*/ && -true/*-1*/ + (+undefined)/*NaN*/ + ""（将前面的部分都转换为字符串）){
        document.write('TEST1');// 能够打印
    }
    if(11 + "11" * 2 == 33){//ture（左侧先转换为Number的33）
        document.write('TEXT2');
    }
    !!" "/*true*/ + !!""/*false*/ - !!false||document.write('TEXT3');(左边等于1，||右边截断，TEXT3不打印)
```

> 不发生类型转换
    === （绝对等于）
    !== （绝对不等于）

<!--
当一个变量未定义时，当且仅当只有一种情况不报错
```JS
    typeof(a)（返回undifined）
```
-->

## 函数

### 特点
高内聚、弱耦合

### 定义（函数声明）

1、命名函数表达式
```JS
    function test(){
        /*blank */
    }
```
2、匿名函数表达式---函数表达式
```JS
    var TEXT = function test(){
        /*blank */
    }
    //(此时 TEXT.name 为 test)
    //TEXT.lengh的值为形参的数量
```

### 参数(实参 与 形参)
JavaScript中函数天生**不定参**
```JS
    function test(a, b){//此处已经隐式var了形参
        /*blank */
    }
```

### arguments
实参列表

### 映射
1. 形参变时，arguments中对应的数值也会发生变化，但两者并不是同一个变量，只是由系统内的映射规则绑定在了一起

2. 实参列表中的元素数量同实参的数量相同，只有满足实参与形参对应的元素受映射规则的约束

### 全局变量

### 局部变量

<!-- 递归： 找规律 找出口 -->

### 函数可嵌套
```JS
    function fun1(){
        /*blank */
        function fun2(){
            /*blank */
        }
    }
```

## 语法分析

### 预编译

#### 规则
1. 函数声明整体提升

2. 变量 声明提升

3. imply global 暗示全局变量：即任何变量，如果变量未经声明就赋值，此变量就为全局对象所有
```JS
    a = 10;
        --->window.a = 10;
```
4. 一切声明的全局变量，全是window的属性
```JS
    var b = 10;
        --->window.b = 10;
```
<!-- window 就是全局的域（window就是全局） -->

//在函数中取变量值，优先取AO，AO没有再查找GO

//解释执行: 在预编译过程中已经看过的语句将会被忽略

#### 预编译过程

##### 函数内的预编译过程
//预编译发生在函数执行的前一刻
1. 创建AO对象(Activation Object(活跃对象)（执行期上下文）)
```JS
    AO{
        /*blank*/
    }
```
2. 找形参和变量声明，将变量和形参名作为AO属性名，值undefined  (即使声明是在if等语句里面也要直接取出)
```JS
    AO{
        a : undefined,
        b : undedined,
        ……
    }
```
4. 将实参值和形参统一
    …………
5. 在函数体里面找函数声明，值赋予函数体
    （若出现同名，先前的数据将会被覆盖）

##### 全局的预编译过程
//GO比AO先执行
1、生成了一个GO（Global Object）对象
2、
```JS
GO{
    a : undefined,
}
// window === GO
```
3、在函数体里面找函数声明，值赋予函数体

例1：
```JS
    function bar(){
        return foo;
        foo = 10;
        function foo(){
            /*blank*/;
        }
        var foo = 11;
    }
    console.log(bar());

    分析：
        GO{
            bar : undefined --> (){/*blank*/}
        }

        AO{
            foo : undefined --> (){/*blank*/}
        }

    答案：打印函数
```
例2：
```JS
    a = 100;
    function demo(e) {
        function e() {
            arguments[0] = 2;
            document.write(e);
            if(a) {
                var b = 123;
                function c() {
                    //注意！！：现在谷歌内核已经不允许在if语句中定义函数！
                }
            }
            var c;
            a = 10;
            var a;
            document.write(b);
            f = 123;
            document.write(c);
            document.write(a);
        }
        var a;
        demo(1);
        document.write(a);
        document.write(f);
    }

    分析：
        GO{
            a : undefined --> 100,
            demo : function() {},
            f : 123,
        }

        在执行到demo(1)的基础上开始分析demo()的AO：
        AO{
            e : undefined --> 1 --> function() {} --> 2（因为arguments[0]与e相映射）,
            b : undefined,
            c : undefined --> (function() {}),
            a : undefined --> 10,
        }

    答案：
        a = 100;
        function demo(e) {
            function e() {
                arguments[0] = 2;
                document.write(e);//2
                if(a) {
                    var b = 123;
                    function c() {
                        //注意！！：现在谷歌内核已经不允许在if语句中定义函数！
                    }
                }
                var c;
                a = 10;
                var a;
                document.write(b);//undefined
                f = 123;
                document.write(c);//undefined (function(在谷歌以前的版本中))
                document.write(a);//10
            }
            var a;
            demo(1);
            document.write(a);//100
            document.write(f);123
        }
```

## 作用域精解

### [[scope]]

每个JavaScript函数都是一个对象，对象中有些属性我们可以访问，但有些不可以，
这些属性仅供JavaScript引擎存取，[[scope]]就是其中一个。（隐式属性）
[[scope]]指的就是我们所说的作用域，其中存储了运行期上下文的集合

### 作用域链

[[scope]]中所存储的执行期上下文对象的集合，这个集合呈链式连接，我们把这种链式连接叫做作用域链

### 运行期上下文

当函数执行前一刻，会创建一个称为执行器上下文的内部对象。

一个执行期上下文定义了一个函数执行时的环境，
函数每次执行时对应的执行上下文都是独一无二的，所以多次调用一个函数会导致创建多个执行期上下文，
当函数执行完毕，将该函数所产生的执行期上下文将被销毁

### 查找变量

从当且执行函数的作用域链的顶端依次向下查找

### 函数的连续执行

```JS
var obj = {
    fun1 : function () {
        console.log('TEST1');
        return this;
    },
    fun2 : function () {
        console.log('TEST2');
        return this;
    }
}
obj.fun1().fun2();
```

### 例题
```JS
例：
    function a() {
        function b() {
            var bb = 234;
        }
        var aa = 123;
        b();
    }
    var glob = 100;
    a();

    //a defiened a.[[scope]] -->
    0 :
    GO {……}

    //a doing a.[[scope]] --- >
    0 :
    AO {
        this : window,
        window : (object),
        document : (object),
        aa : 123,
        b : (function),
    }

    1 :
    GO {
        this : window,
        window : (object),
        documents : (object),
        a : (function),
        glob : 100,
    }

    //b doing b.[[scope]] --- >
    0 :
    AO {//b的AO是在a的作用域链的基础上建立的（并且这是在b执行的时候建立的，注意并不是在定义的时候）
        this : window,
        window : (object),
        bb : 234,
    }

    1 :
    AO {//b所访问的这个AO就是先前a所创建的AO
        this : window,
        window : (object),
        document : (object),
        aa : 123,
        b : (function),
    }

    2 :
    GO {
        this : window,
        window : (object),
        documents : (object),
        a : (function),
        glob : 100,
    }
```

```JS
例:
    function a() {
        function b() {
            function c() {}
            c();
            c();
        }
        b();
    }
    a();

    过程:
    a defined a.[[scope]] --> 0 : GO

    a doing   a.[[scope]] --> 0 : aAO   1 : GO

    b defined b.[[scope]] --> 0 : aAO   1 : GO

    b going   b.[[scope]] --> 0 : bAO   1 : aAO   2 : GO

    c defined c.[[scope]] --> 0 : bAO   1 : aAO   2 : GO

    c going1   c.[[scope]] --> 0 : cAO   1 : bAO   2 : aAO   3 : GO

    c going2   c.[[scope]] --> 0 : NEWcAO   1 : bAO   2 : aAO   3 : GO
```

## 立即执行函数（针对初始化功能的函数）

### 定义

此类函数没有声明，在一次执行过后立即释放。适合用于做初始化工作。

### 书写格式

```JS
    result/*接受结果*/ = (function (/*形参列表*/) {//函数名可写可不写，因为该函数在执行完一次之后将会被立即销毁，无法再通过名字来调用
        /*blank*/
        return /*结果*/
    }(/*传入实参列表*/))
```

1. (function(){}());//推荐使用这种写法
2. (function(){})();

### 相关
1. 只有表达式才能被执行符号执行
2. 能被执行符号执行的表达式，这个表达式的名字就会被自动忽略
```JS
    var test = function() {
        console.log('a');
    }()//函数表达式能够被执行，并且由于函数的名称被忽略，test将不代表函数
```
3. 在函数声明前加上 +、-、！、&&、|| 并且在声明的末尾加上 () 都能够将它变为立即执行函数
<!--
    (function test() {}) 外层的()将整个式子变为表达式
        因此该式能够直接执行 (function test() {})()//最后的括号能够放入前面的括号里，根据括号执行的优先顺序不影响立即执行函数的执行
-->
4. 立即执行函数中的this指向全域，即window（es3.0）

## 闭包

closure(a function which over the environment（scope）in which it was defined)//在一个封闭的词法作用域中，将f某些自由变量包在定义它的函数中

> 内部的函数被保存到了外部一定生成闭包

```JS
    例:
        function a() {
            function b() {
                var bbb = 234;
                console.log(aaa);
            }
            var aaa = 123;
            return b;
        }
        var glob = 100;
        var demo = a();
        demo();//123

        function a() {
            var num = 100;
            function b() {
                num ++;
                console.log(num);
            }
            return b;
        }
        var demo = a();
        demo();//101
        demo();//102
```

### 闭包的危害

当内部函数被保存到外部时，将会生成闭包。
闭包会导致原有作用域链不释放，造成内存泄露。

### 闭包的作用

1. 实现共有变量 eg：函数累加器
```JS
            funtion add() {
                var count = 0;
                function demo() {
                    count++;
                    console.log(count);
                }
                return demo;
            }

            car counter = add();
            counter();

```
2.可以做缓存（储存结构）eg：eater
```JS
        function test() {
            var num = 100;
            function a() {
                num++;
                console.log(num);
            }
            function b() {
                num--;
                console.log(num);
            }
            return [a,b];
        }
        var myArr = test();
        myArr[0]();//101
        myArr[1]();//100
```
```JS
        function eater() {
            var food = "";
            var obj = {
                eat : function (){//对象里面也是可以有函数的
                    console.log("I am eatin " + food);
                    food = "";
                },
                push : function (myFood){
                    food = myFood;
                }
            }
            return obj;
        }

        var eater1 = eater();

        eater1.push('banana');
        eater1.eat();
```

3. 可以实现封装，属性私有化 eg：Person();

```JS
function test(data) {
    var pre = 'preData';
    this.data = data;
    this.changeData = function () {
        this.data = pre;
    }
    this.changePre() = function (newData) {
        pre = newData;
    }
    this.showPredata = function () {
        console.log(pre);
    }
}
var test = new test('data');
console.log(test.data); // 'data'
console.log(test.showPredata()); // 'perData'
test.changeData();
console.log(test.data); // 'preData'
test.changePre('newPredata');
console.log(test.showPredata()); // 'newPredata'
console.log(test.pre) // undifined

// 构造函数中的函数属性被保存到了函数外部形成了闭包,因此能test能够在函数外部调用到pre的值
// 但pre这一属性本身并不存在于新构造的对象test中,pre只能够通过对象中的方法进行调用,从而实现了属性的私有化
```

4. 模块化开发，防止污染全局变量

### 闭包导致的错误：
```JS
    function test() {
        var arr = [];
        for(var i = 0; i < 10; i++) {
            arr[i] = function() {
                document.write(i + " ");
            }
        }
        return arr;
    }
    var myArr = test();
    for(var j = 0; j < 10; j++) {
        myArr[j]();
    }

    运行结果:10 10 10 10 10 10 10 10 10 10

    解决方案:
    function test() {
        var arr = [];
        for (var i = 0; i < 10; i++) {
            (function (j) {
                arr[j] = function () {
                    document.write(j + " ");
                }
            }(i));
        }
        return arr;
    }
    var myArr = test();
    for (var j = 0; j < 10; j++) {
        myArr[j]();
    }
```

<!-- 逗号操作符（实际运用与 C语言 相似） -->

## 对象

### 主要考察

属性的 增 删 改 查

### 对象的创建方法

#### 直接创建

var obj = {} plainObject 对象字面量/对象直接量

#### 构造函数

<!-- 构造函数在形式上与函数格式相同 -->
<!-- 为避免混淆，构造函数在命名时必须使用大驼峰式命名规则 -->


##### 系统自定义的构造函数

（1）new Object() Array() Number()
```JS
var obj = new Object();
```

（2）自定义

**构造函数的内部原理**
1. 在函数体最前面隐式加上this = {}
2. 执行 this.xxx = xxx;
3. 隐式地返回this

```JS
function Car(color) {
    //var this = {
        /*内容*/
    //};    (隐式声明)
    this.color = color;
    this.name = "BMW";
    this.height = "1400";
    this.health = 100;
    this.run = function() {
        this.health --;
    }
    //return this;（隐式返回）
}
var car = new Car('red');//（当函数前有 new 时，函数返回的必是对象，这与用户是否在function的末尾自行添加return无关）
```

### 包装类

new Number String Boolean

例：
```JS
var num = 4;
num.len = 3;
//new Number(4).len = 3; //隐式声明
//delete; //自行销毁隐式对象
console.log(num.len);//运行结果：系统不进行报错，输出undefined

// 这一隐式执行过程被称为包装类
```


#### Str.length的执行原理

**原始值一定不包含属性**

str.length能够返回字符串的原理为系统生成了一个String的包装类，返回的为包装类内的length值

```JS
// str.length原理
var str = 'abcd';
// new String('abcd').length（隐式进行）
console.log(str.length);// 4
```

例题
```JS
var str = 'abc';
str += 1;// str == 'abc1'
var test = typeof(str);// test == 'String'
if(test.length == 6) {
    test.sign = 'typeof的返回结果可能为String'
}
// new String(test).sign
console.log(test.sign);// Answer：undefined
```

#### 原始值转换为包装类

```JS
var num =1;
num = new Number(num);
```

### 属性的查看方法

```JS
var obj = {
    elm1 : {test1 : 'element1'},
    elm2 : {test2 : 'element2'},
    showElm : function(num) {
        return this['elm'+num];
    }
}
obj.showElm(1);
// 隐式转换 obj.elm1 ----> obj['elm1'] （[] 中必须为字符串）


```

### 例题

```JS
function Person(name, age, sex) {
    var a = 0;
    this.name = name;
    this.age = age;
    this.sex = sex;
    function sss() {
        a ++;
        console.log(a);
    }
    this.say = sss;
}

var oPerson = new Person();
oPerson.say();// 1
oPerson.say();// 2
var yPerson = new Person();
yPerson.say();// 1
```

## 原型

### 定义

原型是function的一个属性，它定义了构造函数制造出的对象的公共祖先。
通过该构造函数产生的对象，可以继承该原型的属性和方法。
原型也是对象。





对象如何查看对象的构造函数 --> constructor

```JS
// Person.prototype -- 原型 系统所自带的空对象
// Person.prototype = {}
Person.prototype.name = "Hello world!"
function Person() {
    // blank
}

var person1 = new Person();
console.log(person1.name);// Hello world!

var person2 = new Person();
console.log(person2.name);// Hello world!

// person1与 person2 中都并非实际含有name属性,而是借用(访问)了原型中的属性
```

```JS
Person.prototype.name = "Hello world!";
function Person() {
    this.name = "Gura!"
}

var person = new Person();
console.log(person.name);// Gura!

// 当原型中的属性与对应的构造函数中的属性中冲突时,使用构造函数中定义的属性值
```

### 原型的增删改查

```JS
Person.prototype = {
    name : "A",
    sex : "male",
}
function Person() {}
var person = new Person();
Person.prototype.name = "B"; // 改
Person.prototype.age = 13; //增
delete(Person.prototype.sex);// 删
console.log(Person.prototype);
// 其余操作均与一般对象的增删改查类似

// 对象如何查看对象的原型 --> 隐式属性 __proto__
console.log(person.__proto__);
function Student() {
    var this = {//隐式
        __proto__: Student.prototype // 当访问对象的属性时，若该对象中没有对应的属性，系统将会通过__proto__的索引找到__ptoto__所指向的原型，并在该原型中寻找该属性（相当于与原型之间的桥梁）
    }
}

//对象如何查看对象的构造函数 --> constructor
funtion Car() {
}
var car = new Car();
console.log(car.constructor);//返回该对象的构造函数（初始时由系统自动生成，但可以手动更改）
```

```JS
// 陷阱题
Person.prototype.name = 'sunny';
function Person() {
    // var this = {__proto__: Person.prototype}//指向一个空间
}

var person = new Person();
Person.prototype = {//换了一个空间，但此时__proto__所指向的仍为原来的空间
    name : 'cheery'
    }

console.log(person.name) // sunny
```

```JS
Person.prototype.name = 'sunny';
funtion Person() {
    //
}

Person.prototype = {
    name : 'cheery'
}

var person = new Person();

console.log(person.name);// cheery（注意不同书写顺序下各语句的执行顺序）
```


### 应用

利用原型的特点，可以提取共有属性

绝大多数对象最终都会继承自Object.prototype
<!-- 特例：Object.create(null) -->

### 原型链

原型链的访问结点即为 __proto__

```JS
Grand.prototype.lastName = "Garw";
function Grand() {

}
var grand = new Grand();

Father.prototype = grand;
function Father() {

}
var father = new Father();

Son.prototype = father;
function Son() {

}
var son = new Son();

console.log(son.lastName);

// 原型链的终端为 Object{}
```

```JS
// a.sayName()
// sayName里面的this指向是，谁调用这个方法，this就指向谁
Person.ptrotype = {
    name : "Gura",
    sayName : function () {
        console.log(this.name);
    }
}
function Person() {
    this.name = "Ame"
}
var person = new Person();

person.sayName();// Ame
Person.prototype.sayName();// Gura
```

#### 原型链的增删改查

与原型类似

特例：
```JS
function Father() {
    this.fortune = {
        card1 : "Visa"
    }
}
var father = new Father();

Son.preototype = father;
function Son() {

}
var son = new Son();

son.fortune.card2 = 'Master'// 调用形式的修改是可行的
```

#### Object.create()

```JS
// var obj = Object.create(原型);
var obj = {name : "sunny", age : 123};
var obj1 = Object.create(obj);// obj1的原型即为obj
```

#### 方法的重写

同名不同功能的方法，覆盖终端的方法
<!-- 重写是一个很泛的概念 -->


## JavaScript中的BUG

JS在浮点数计算的过程中通常存在有**精度偏差**
<!-- （可正常计算的范围 小数点前16位与后16位） -->
<!-- 可通过 0.14 * 100 进行验证 -->
因此在需要进行浮点计算时往往需要结合取整方法

### toFixed()
保留两位小数

### Math.ceil
向上取整方法
```JS
Math.ceil(123.1) // 124
```

### Math.floor
向下取整方法
```JS
Math.ceil(123.9) // 123
```

## call/apply

### 作用
改变this指向

```JS
function Person(name,age) {
    // this == obj（隐式）
    this.name = name;
    this.age = age;
}
var person = new Person('Garw Gura', 9000);

var obj = {
}
Person.call(obj, 'Mumei', '20');
// 函数执行默认为call（ 即：test() --> test.call() ）
```

```JS
// 应用
function Person(name, age, sex) {
    this.name = name;
    this.age = age;
    this.sex = sex;
}

function Student(name, age, sex, tel, grade) {
    Person.call(this, name, age, sex); // 实现借用别人的函数实现自己的功能的封装
    this.tel = tel;
    this.grade = grade;
}

var student = new Student('sunny', 123, 'male', 139, 2017);
```

### 区别

**传参列表不同**

call 需要把实参按照形参的个数传进去
apply 只能包含一个实参，且该实参必须为arguments（数组）

```JS
function Person(name,age) {
    this.name = name;
    this.age = age;
}

var obj = {};
var obj1 = {};

Person.call(obj, 'name', 0)
Persin.apply(obj1, ['name', 0])
```