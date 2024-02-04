public class Employee {
    String name;
    int age;
    String designation;
    double salary;
    // Employee class constructor
    public Employee(String name) {
        this.name = name;
    }

    public void empAge(int empAge) {
        age = empAge;
    }

    public void empDesignation(String empDesig) {
        designation = empDesig;
    }

    public void empSalary(double empSalary) {
        salary = empSalary;
    }

    public void printEmployee() {
        System.out.println("name:" + name);
        System.out.println("age:" + age);
        System.out.println("designation:" + designation);
        System.out.println("salary:" + salary);
    }
}
