package practice;

public enum AbstractEnumDemo {
    X() {
        @Override
        public void doSomething() { }
    }, Y() {
        @Override
        public void doSomething() { }
    };

    public abstract void doSomething();

}

