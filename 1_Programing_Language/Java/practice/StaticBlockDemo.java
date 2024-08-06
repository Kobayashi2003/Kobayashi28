package practice;

public class StaticBlockDemo {

    static int number = 10;

    private StaticBlockDemo() {
        /* prevent instantiation */ }

    static {
        System.out.println("Hello from static block.");
    }

}
