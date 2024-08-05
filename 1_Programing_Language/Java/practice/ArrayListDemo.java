import java.util.ArrayList;
import java.util.Random;

public class ArrayListDemo {
    public static void main(String[] args) {
        // ArrayList<String> list = new ArrayList<String>();
        ArrayList<String> list = new ArrayList<>(); // support after jdk 1.7
        list.add("Hello");
        list.add("World");
        list.add("Java");

        for (int i = 0; i < list.size(); ++i) {
            System.out.println(list.get(i));
        }

        ArrayList<Integer> number_list = new ArrayList<>();
        Random random = new Random();

        for (int i = 0; i < 100; ++i) {
            number_list.add(random.nextInt(100));
        }

        // delete all numbers that are greater than 50
        for (int i = number_list.size() - 1; i >= 0; --i) {
            if (number_list.get(i) > 50) {
                number_list.remove(i);
            }
        }

        for (int i = 0; i < number_list.size(); ++i) {
            System.out.print(number_list.get(i) + " ");
        }
    }
}