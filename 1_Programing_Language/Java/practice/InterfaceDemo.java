package practice;

public interface InterfaceDemo {
    String NAME = "InterfaceDemo";

    void test(); // abstract method

    public default void test1() { // after JDK 8
        System.out.println("test1");
    }

    // private void test2() { // after JDK 9
    //     System.out.println("test2");
    // }

    public static void test3() { // after JDK 8
        System.out.println("test3");
    }
}
