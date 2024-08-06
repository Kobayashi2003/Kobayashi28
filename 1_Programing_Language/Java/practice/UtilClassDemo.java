import java.util.ArrayList;

public class UtilClassDemo {

    private UtilClassDemo() { /* prevent instantiation */ }

    public static void printList(ArrayList<String> list) {
        for (int i = 0; i < list.size(); ++i) {
            System.out.println(list.get(i));
        }
    }    
}
