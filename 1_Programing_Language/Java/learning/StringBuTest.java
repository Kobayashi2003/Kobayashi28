public class StringBuTest {
    public static void main(String[] args) {
        StringBuilder sb = new StringBuilder(10);
        sb.append("Runoob..");
        System.out.println(sb);
        sb.append("!");
        System.out.println(sb);
        sb.insert(8, "Java");
        System.out.println(sb);
        sb.delete(5, 8);
        System.out.println(sb);

        StringBuffer sBuffer = new StringBuffer("hello");
        sBuffer.append(" ");
        sBuffer.append("java");
        sBuffer.append("!");
        System.out.println(sBuffer);
    } 
}
