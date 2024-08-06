package practice;

public class SingleInstanceDemo {

    private static SingleInstanceDemo instance = new SingleInstanceDemo();

    private SingleInstanceDemo() {
       /* prevent instantiation */ }

    public static SingleInstanceDemo getInstance() {
        return instance; }

    /** LAZY INITIALIZATION
     * private static SingleInstanceDemo instance = null;
     * 
     * private SingleInstanceDemo() { }
     * 
     * public static SingleInstanceDemo getInstance() {
     *     if (instance == null) {
     *         instance = new SingleInstanceDemo();
     *     }
     *     return instance;
     * }
     */
}
