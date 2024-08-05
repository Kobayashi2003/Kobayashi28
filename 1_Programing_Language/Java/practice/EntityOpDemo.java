public class EntityOpDemo {
    private EntityDemo entity; 

    public EntityOpDemo() { }
    public EntityOpDemo(EntityDemo entity) { this.entity = entity; }

    public void showData() {
        System.out.println(entity.getData());
    }
}

