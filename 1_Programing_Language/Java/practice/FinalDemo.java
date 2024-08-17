package practice;

public class FinalDemo {
    public static void main(String[] args) {
        System.out.println(Utils.add(1, 2));    
    }
}

final class Utils {
    public static int add(int a, int b) {
        return a + b;
    }
}

class Utils2 {
    public final int add(int a, int b) {
        return a + b;
    }
    public int sub(final int a, final int b) {
        return a - b;
    }
}

class Utils3 {
    public static final int id = 1;
}
