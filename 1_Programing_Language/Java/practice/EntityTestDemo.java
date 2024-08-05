public class EntityTestDemo {
    public static void main(String[] args) {
        EntityDemo entity = new EntityDemo();
        EntityOpDemo op = new EntityOpDemo(entity);
        entity.setData(10);
        op.showData();        
    }
}
