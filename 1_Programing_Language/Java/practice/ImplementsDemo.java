package practice;

public class ImplementsDemo implements InterfaceDemo {
    public static void main(String[] args) {
        System.out.println(Utils.add(1, 2));
    }

    @Override
    public void test() {
        System.out.println("test");
    }
}
