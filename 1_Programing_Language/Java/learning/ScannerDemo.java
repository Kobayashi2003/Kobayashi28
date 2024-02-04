import java.util.Scanner;

public class ScannerDemo {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        if (scan.hasNext()) {
            String str = scan.next();
            System.out.println(str);
        }

        scan.close();
    }
}
