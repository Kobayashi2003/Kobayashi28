class Student {
private:
    int _num;
    std::string _name;
    char _sex;
public:
    void set_value(int num, std::string name, char sex);
    void display() const;
};