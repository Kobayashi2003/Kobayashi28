public class TestArray {

    public static void reverse(double [] list) {
        int len = list.length;
        for (int i = 0; i < len / 2; ++i) {
            double temp = list[i];
            list[i] = list[len-i-1];
            list[len-i-1] = temp;
        }
    }


    public static void main(String[] args) {
        int size = 10;
        double [] myList = new double[size];

        for (int i = 0; i < size; ++i) 
            myList[i] = i + 0.1;

        for (double num : myList)
            System.out.print(num + " ");
        System.out.println();

        reverse(myList);

        for (double num : myList)
            System.out.print(num + " ");
        System.out.println();
    }
}
