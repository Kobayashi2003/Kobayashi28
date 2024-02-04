class SuperClass {
    private int n;
    SuperClass() {
        System.out.println("SuperClass()");
    }
    SuperClass(int n) {
        System.out.println("SuperClass(int n)");
        this.n = n;
    }
}

class SubClass extends SuperClass {
    private int n;
    SubClass() {
        System.out.println("SubClass");
    }

    SubClass(int n) {
        super(300);
        System.out.println("SubClass(int n):" + n);
        this.n = n;
    }
}  

class SubClass2 extends SuperClass {
    private int n;
    SubClass2() {
        super(300);
        System.out.println("SubClass2");
    }
    SubClass2(int n) {
        System.out.println("SubClas(int n):" + n);
        this.n = n;
    }
}


public class TestSuperSub {
    public static void main(String[] args) {
        System.out.println("-----SubClass-----");
        SubClass sc1 = new SubClass();
        SubClass sc2 = new SubClass(100);
        System.out.println("-----SubClass2-----");
        SubClass2 sc3 = new SubClass2();
        SubClass2 sc4 = new SubClass2(200);
    } 
}
