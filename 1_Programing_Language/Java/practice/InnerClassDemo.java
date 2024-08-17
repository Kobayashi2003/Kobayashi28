package practice;

public class InnerClassDemo {
    public static void main(String[] args) {
        OuterClass outer = new OuterClass();
        OuterClass.InnerClass inner = outer.new InnerClass();
        inner.doSomething();
    } 
}

class OuterClass {
    public static int num = 1;
    class InnerClass {
        // public static String str = "hello"; // support after JDK16
        private int num = 2;
        public void doSomething() {
            int num = 3;
            System.out.println(num);
            System.out.println(this.num);
            System.out.println(OuterClass.num);
            System.out.println(OuterClass.this.num);
        }
    }
}
