// TIPs: string object is a unchangeable object

public class StringDemo {
    public static void main(String[] args) {
        String str = "Hello, World!";
        System.out.println(str);

        for (int i = 0; i < str.length(); ++i) {
            System.out.print(str.charAt(i));
        }
        System.out.println();

        str = str.replace("World", "Java");
        System.out.println(str);
    }
}
