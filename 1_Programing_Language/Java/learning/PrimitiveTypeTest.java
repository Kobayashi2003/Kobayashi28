public class PrimitiveTypeTest {

    static boolean bool;
    static byte by;
    static char ch;
    static double d;
    static float f;
    static int i;
    static long l;
    static short sh;
    static String str;

    public static void main(String[] args) {

        final double PI = 3.14;
        int decimal = 100;
        int octal = 0144;
        int hexa = 0x64;

        // byte
        System.out.println(Byte.SIZE);
        System.out.println("java.lang.Byte");
        System.out.println(Byte.MIN_VALUE);
        System.out.println(Byte.MAX_VALUE);
        System.out.println(bool);

        // Short
        System.out.println(Short.SIZE);
        System.out.println("java.lang.Short");
        System.out.println(Short.MIN_VALUE);
        System.out.println(Short.MAX_VALUE);
        System.out.println(sh);

        // long 
        System.out.println(Long.SIZE);
        System.out.println("java.lang.Long");
        System.out.println(Long.MIN_VALUE);
        System.out.println(Long.MAX_VALUE);
        System.out.println(l);

        // float
        System.out.println(Float.SIZE);
        System.out.println("java.lang.Float");
        System.out.println(Float.MIN_VALUE);
        System.out.println(Float.MAX_VALUE);
        System.out.println(f);

        // double
        System.out.println(Double.SIZE);
        System.out.println("java.lang.Double");
        System.out.println(Double.MIN_VALUE);
        System.out.println(Double.MAX_VALUE);
        System.out.println(d);

        // char
        System.out.println(Character.SIZE);
        System.out.println("java.lang.Character");
        System.out.println((int)Character.MIN_VALUE);
        System.out.println((int)Character.MAX_VALUE);
        System.out.println(ch);

    }
}