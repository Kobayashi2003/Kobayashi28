import java.util.Scanner;

public class ScannerDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in); 

        System.out.println("Please input your name: ");
        String name = scanner.nextLine();
            
        System.out.println("Please input your age: ");
        int age = scanner.nextInt();

        System.out.println("Your name is " + name + ", and your age is " + age);

        scanner.close();
    }
}
