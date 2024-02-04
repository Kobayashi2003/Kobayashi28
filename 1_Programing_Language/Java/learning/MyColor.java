enum Color {
    RED, GREEN, BLUE;

    private Color() {
        System.out.println("Constructor called for : " + this.toString());
    }

    public void colorInfo() {
        System.out.println("Universal Color");
    }
}

public class MyColor {
    public static void main(String[] args) {
        Color myVar = Color.BLUE;

        System.out.println(myVar);
        myVar.colorInfo();

        switch (myVar) {
            case RED:
                System.out.println("RED");
                break;
            case GREEN:
                System.out.println("GREEN");
                break;
            case BLUE:
                System.out.println("BLUE");
                break;
        
            default:
                break;
        }

        Color[] arr = Color.values();

        for (Color col : arr) {
            System.out.println(col + " at index " + col.ordinal());
        }

        System.out.println(Color.valueOf("RED"));
    } 
}
