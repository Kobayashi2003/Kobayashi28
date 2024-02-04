public class RunoobTest {
    private int instanceVar;
    private static int staticVar;

    public void method(int paramVar) {
        int localVar = 10;
        instanceVar = localVar;
        staticVar = paramVar;

        System.out.println(instanceVar);
        System.out.println(staticVar);
        System.out.println(paramVar);
        System.out.println(localVar);
    }

    public static void main(String[] args) {
        RunoobTest v = new RunoobTest();
        v.method(20); 
    }
}
