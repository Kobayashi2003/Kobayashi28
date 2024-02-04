public class Animal {
    private String name;
    private int id;
    public Animal(String myName, int myId) {
        name = myName;
        id = myId;
    }
    public void eat() {
        System.out.println(name + "eating");
    }
    public void sleep() {
        System.out.println(name + "sleeping");
    }
    public void introduction() {
        System.out.println(name + " " + id);
    }
}