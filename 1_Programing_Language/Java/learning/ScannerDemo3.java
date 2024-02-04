import java.util.Scanner;

public class ScannerDemo3 {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        System.out.println("Please input an integer: ");
        if (scan.hasNextInt()) 
            System.out.println("input integer: " + scan.nextInt());
        else
            System.out.println("not an integer");

        System.out.println("Please input a float: ");
        if (scan.hasNextFloat()) 
            System.out.println("input float: " + scan.nextFloat());
        else 
            System.out.println("not a float");
        
    } 
}
