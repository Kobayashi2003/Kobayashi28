package practice;

public class PolymorphicDemo {
    public static void main(String[] args) {
        People people = new People();
        People man = new Man();
        People woman = new Woman();
        people.whoami();
        man.whoami();
        woman.whoami();        
    }
    
}

class People {

    public People() {
        System.out.println("People Construct"); }

    public void whoami() {
        System.out.println("People"); }
}

class Man extends People {
    public Man() {
        System.out.println("Man Construct"); }
    
    @Override
    public void whoami() {
        System.out.println("Man"); }
}


class Woman extends People {
    public Woman() {
        System.out.println("Woman Construct"); }

    @Override
    public void whoami() {
        System.out.println("Woman"); }
}

