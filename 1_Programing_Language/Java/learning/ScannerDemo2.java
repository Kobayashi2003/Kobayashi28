import java.util.Scanner;

public class ScannerDemo2 {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        if (scan.hasNextLine()) {
            String str = scan.nextLine();
            System.out.println(str); 
        }

        scan.close();
    }    
}
