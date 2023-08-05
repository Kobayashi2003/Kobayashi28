# Consider alternatives to virtual functions（考虑 virtual 函数以外的其他选择）

- 使用 non-virtual interface（NVI）手法，那是 Template Method 设计模式的一种特殊形式。它以 public non-virtual 成员函数包裹较低访问行的 virtual 函数
- 将 virtual 函数替换为 “函数指针成员变量”， 这是 Strategy 设计模式的一种分解表现形式
- 以 tr1::function 成员变量替换 virtual 函数，因而允许使用任何可调用物搭配一个兼容于需求的签名式


```cpp
class GameCharacter {
public:
    int healthValue() const {
        ...
        int retVal = doHealthValue();
        ...
        return retVal;
    }
private:
    virtual int doHealthValue() const = 0;
};
```

这一基本设计为“令用户通过 public non-virtual 成员函数间接调用 private virtual 函数”，称为``non-virtual interface (NVI)``手法。它是所谓 ``Template Method`` 设计模式的一个实例。书中称这个 non-virtual 成员函数为 virtual 函数的**外覆器（wrapper)**


**藉由 Function Pointers 实现 Strategy 模式**

```cpp
class GameCharacter;
int defaultHealthCalc(const GameCharacter& gc);
class GameCharacter {
public:
    typedef int (*HealthCalcFunc) (const GameCharacter&);
    explicit GameCharacter(HealthCalcFunc hcf = defaultHealthCalc) : healthFunc(hcf) {}
    int healthValue() const {
        return healthFunc(*this);
    }
    ...
private:
    HealthCalcFunc healthFunc;
};
```

这个做法是常见的 Strategy 设计模式的简单应用。它提供了一种在运行时改变对象行为的方法。

```cpp
class EvilBadGuy : public GameCharacter {
public:
    explicit EvilBadGuy(HealthCalcFunc hcf = defaultHealthCalc) : GameCharacter(hcf) {...}
    ...
};
int loseHealthQuickly(const GameCharacter& gc);
int loseHealthSlowly(const GameCharacter& gc);

EvilBadGuy ebg(loseHealthQuickly);
EvilBadGuy ebg2(loseHealthSlowly);
```

- 某已知人物的健康指数可以在运行期变更

换句话说，“健康指数计算函数不再是 GameCharacter继承体系内的成员函数”。这一事实意味，这些计算函数并未特别访问 “即将被计算健康指数”的那个对象的内部成分。

一般而言，唯一能解决 “需要以 non-member函数访问 class的 non-public成分”的方法就是：**弱化class的封装**


**藉由 tr1::function 完成 Strategy 模式**

```cpp
tr1::function:

    class GameCharacter;
    int defaultHealthCalc(const GameCharacter& gc);
    class GameCharacter {
    public:
        // HealthCalcFunc 可以是任何可调用物（callable entity），可被调用并接受
        // 任何兼容与 GameCharacter 之物，返回任何兼容于 int 的东西
        typedef std::tr1::function<int (const GameCharacter&)> HealthCalcFunc;
        explicit GameCharacter(HealthCalcFunc hcf = defaultHealthCalc) : healthFunc(hcf) {}
        int healthValue() const {
            return healthFunc(*this);
        }
    private:
        HealthCalcFunc healthFunc;
    };
```

和前一个设计比较，这个设计唯一不同的是如今 GameCharacter 持有一个 tr1::function 对象，相当于一个指向函数的泛化指针。