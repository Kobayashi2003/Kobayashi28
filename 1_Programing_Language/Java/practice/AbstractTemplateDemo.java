package practice;

public class AbstractTemplateDemo {
    public static void main(String[] args) {
        new SonClass().doSomething();        
    }    
}


abstract class FatherClass {
    public void doSomething() {
        sayHello();        
    }

    public abstract void sayHello();
}

class SonClass extends FatherClass {
    public void sayHello() {
        System.out.println("Hello");
    }
}
