package practice;

public class ConstructorDemo {
    public static void main(String[] args) {
        Son son = new Son();
    }
}

class Father {

    public Father() {
        this(0); }

    public Father(int x) {
        System.out.println("Father"); }

}

class Son extends Father {

    public Son() {
        super(1);
        System.out.println("Son");
    }

}