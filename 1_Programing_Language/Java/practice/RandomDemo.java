import java.util.Random;
import java.util.Scanner;

public class RandomDemo {
    public static void main(String[] args) {
        Random random = new Random();
        Scanner scanner = new Scanner(System.in);

        int number = random.nextInt(10) + 1;

        while (true) {
            System.out.println("Guess a number between 1 and 10: ");
            if (scanner.nextInt() == number) {
                System.out.println("You guessed correctly!");
                break;
            } else {
                System.out.println("Try again!");
            }
        }

        scanner.close();
    }
}
