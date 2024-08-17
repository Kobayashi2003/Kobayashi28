package practice;

public class AnonymousInnerClass {
    public static void main(String[] args) {
        AbstractClass a = new AbstractClass() {
            @Override
            public void doSomething() {
                System.out.println("Hello");
            }
        };
        a.doSomething();
    }    
}

abstract class AbstractClass {
    public abstract void doSomething();
}