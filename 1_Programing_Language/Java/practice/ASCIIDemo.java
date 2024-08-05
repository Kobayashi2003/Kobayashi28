public class ASCIIDemo {
    public static void main(String[] args) {
        System.out.println((char)('a' + 10)); 
        System.out.println((char)('A' + 10));
        System.out.println('0' + 9);
        
        System.out.println(0B10);
        System.out.println(010);
        System.out.println(0X10);

        int num = 5;
        System.out.println("abc" + num);
        System.out.println(num + "abc");
        System.out.println("abc" + num + 'a' + "abc");
        System.out.println(num + 'a' + "abc");
    }
}
