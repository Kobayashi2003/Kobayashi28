#include<iostream>
#include<cstring>
#include<vector>

#define dataType int

using namespace std;

typedef unsigned long long int ULL;


/* Queue declaration */

template <typename Type>
class Queue {
public :
    class Node; // nested class

private :
    enum {MAX = 5, MIN = 1, Limit = 100};
    Node * front; // pointer to front of Queue
    Node * rear; // pointer to back of Queue
    int items; // current number of items in Queue
    int qsize; // maximum number of items in Queue

protected :

    /* protected methods */

    // bool error(int num) { // error checking
    //     if(num < MIN) {
    //         cout << "error" << endl
    //         return false;
    //     }
    //     return true;
    // }

    bool errorSize(int & size) { // to judge if the size of the queue is too small
        try {
            if (size < MIN) {
                throw "the size of Queue is less than the minimum, please enter a new size";
            }
        } catch (const char * errMsg) {
            cerr << errMsg << endl;
            cin >> size;
            qsize = size;
            return errorSize(size);
        }
        return true;
    }

    bool confirm() const { // last confirm
        char flag;
        cout << "[please input Y/N](Yes/No): ";
        cin >> flag;
        cin.ignore(std::numeric_limits<streamsize>::max());
        if (cin.rdstate()) {
            cin.ignore(std::numeric_limits<streamsize>::max(), '\n');
            cout << "stream clear" << endl;
        }
        return (flag == 'y' || flag == 'Y');
    }

    /* Linked List methods */
    Queue * createLinkedList(); // create a blank linked list
    Queue * createLinkedList(vector <Type> & Items); // create a Linked List by using the data in vector

    Queue * Anti_Link(); // anti link the linked List

    Queue * layout(); // layout the linked List

public :

    /* Construct & Destructor */

    // create a blank Queue
    Queue(int size = MAX) : front(nullptr), rear(nullptr), items(0), qsize(size){ // construcotr
        cout << "Queue constructor" << endl;
        errorSize(size);
        createLinkedList() -> Anti_Link() -> layout(); // create a Linked List then anti link then layout
    }

    // create a Queue and deposit the data in the vector
    Queue(vector <Type> & Items, int size = MAX) : // constructor
            front(nullptr), rear(nullptr),
            items(Items.size()),
            qsize( ((ULL)size > Items.size() ? size : Items.size()) )
    {
        cout << "Queue constructor" << endl;
        errorSize(size);
        createLinkedList(Items) -> Anti_Link() -> layout(); // create a Linked List then anti link then layout
    }

    ~Queue() { // destructor
        delete rear; // call the destructor of Node to destroy the linked list
        cout << "Queue destructor" << endl;
    }

    /* Public methods */

    // bool extend(int newSize);

    /* read only methods */
    bool isEmpty() const; // if the queue is empty
    bool isFull() const; // if the queue is full
    int queueCount() const; // show the number of items in the queue

    /* enter and remove */
    Queue * enQueue(); // add ghost node to the end
    Queue * enQueue(Type item); // add item to end
    Queue * deQueue(); // remove item from front

    Queue * clear(); // clear the queue

    /* overloaded methods */
    Type & operator[](int num) {
        if (num < front -> update_number() || num > rear -> update_number()) {
            cerr << "this node does not exiet" << endl;
            return rear -> getData();
        }
        Node * find = front;
        while((find -> update_number() != num) && (find != nullptr)) {
            find = find -> getLast();
        }
        return find -> getData();
    }

    friend ostream & operator<<(ostream & os, const Queue & q) {
        q.rear -> showAll();
        return os;
    }
};

// template <typename Type>
// bool Queue<Type>::extend(int newSzie) {
//     if(newSize < qsize) {
//         cout << "the new size is too small" << endl;
//         return false;
//     }
//
//     cout << "Queue extend" << endl;
//
//     Node * newRear, * node;
//     newRear = node = new Node();
//     for(int i = qsize; i < newSize; ++i) {
//         Node * newNode = new Node();
//         node -> connect(newNode);
//         node = newNode;
//     }
//     node -> connect(rear);
//     rear = newRear;
//     qsize = newSize;
//
//     return true;
// }

/* read only methods */
template <typename Type>
bool Queue<Type>::isEmpty() const { // if the queue is empty
    if (items == 0) {
        return true;
    }
    return false;
}

template <typename Type>
bool Queue<Type>::isFull() const { // if the queue is full
    if (items == qsize) {
        return true;
    }
    return false;
}

template <typename Type>
int Queue<Type>::queueCount() const { // show the number of items in the queue
    cout << "used: " << items << endl << "last: " << qsize - items << endl;
    return items;
}


/* Linked List methods */
template <typename Type>
Queue<Type> * Queue<Type>::createLinkedList() {/* create a linked list for Queue */

    rear = new Node(); // the parameters are defaulted to nullptr and (Type)0
    Node * node = rear;
    for(int i = 1; i < qsize; ++i) {
        Node * newNode = new Node();
        node -> connect(newNode);
        node = newNode;
    }
    front = node;
    return this;

}

template <typename Type>
Queue<Type> * Queue<Type>::createLinkedList(vector <Type> & Items) {/* create a linked list for Queue */
    // create a linked list for Queue and set the data of vector in it
    rear = new Node(nullptr, Items[0]);
    Node * node = rear;
    for(int i = 1; (ULL)i < Items.size(); ++i) {
        Node * newNode = new Node(nullptr, Items[i]);
        node -> connect(newNode);
        node = newNode;
    }
    if(Items.size() < (ULL)qsize) {
        // create some blank nodes to fill the queue
        for(int i = (int)Items.size(); i < qsize; ++i) {
            Node * newNode = new Node();
            node -> connect(newNode);
            node = newNode;
        }
    }
    front = node;
    return this;
}

template <typename Type>
Queue<Type> * Queue<Type>::Anti_Link() { // anti link the linked List
    if (rear == nullptr || front == nullptr) {
        cerr << "the queue is non-existent" << endl;
    } else if (rear == front) {
        cerr << "the queue is too short" << endl;
    } else {
        for(Node *p1 = rear, *p2 = rear -> getNext(); p2 != nullptr; p1 = p2, p2 = p2 -> getNext()) {
            p2 -> connect_back(p1);
        }
    }
    return this;
}

template <typename Type>
Queue<Type> * Queue<Type>::layout() { // layout the Linked list
    // set the number of each Nodes
    enum {Initial = 1};
    int num = Initial;
    for(Node *p = front; p != nullptr; p = p -> getLast()) {
        p -> update_number(num ++);
    }
    return this;
}

/* enter and remove */
template <typename Type>
Queue<Type> * Queue<Type>::enQueue() { // add a ghost node to the end

    /* check whether the queue is normal */
    if(rear == nullptr || front == nullptr) { // the case when the queue has not been created
        cerr << "the queue is non-existent" << endl;
        return this;
    } else if (isFull()) { // the case when the queue is full
        cout << "the earlist data will be overwritten, are you sure?" << endl;
        if (!confirm()) { // call the fucntion confirm() to make sure whether overwritten is allowed
            return this;
        }
    }

    /* add a blank node（ghostNode） to the rear of queue（the head of the linked list）*/
    Node * newNode = new Node();
    newNode -> Ghost(); // set the ghost flag to true
    newNode -> connect(rear);
    rear -> connect_back(newNode);
    rear = newNode;

    // delete the front node of the queue to keep the the size
    // and reset the front pointer
    Node * tmp = front;
    front = front -> getLast() -> resetNext();
    delete tmp;

    // the ghostNode will still occupy storage sapce of the queue
    items ++;

    return this -> layout();
}

template <typename Type>
Queue<Type> * Queue<Type>::enQueue(Type item) { // add a item to the end
    /* check whether the queue is normal */
    if(rear == nullptr || front == nullptr) {
        cerr << "the queue is non-existent" << endl;
        return this;
    } else if (isFull()) {
        cout << "the earlist data will be overwritten, are you sure?" << endl;
        if (!confirm()) {
            return this;
        }
    }

    /* add a new item to the rear of queue */
    Node * newNode = new Node(rear, item);
    newNode -> connect(rear);
    rear -> connect_back(newNode);
    rear = newNode;

    Node *tmp = front;
    front = front -> getLast() -> resetNext();
    delete tmp;

    items ++;

    return this -> layout();
}

template <typename Type>
Queue<Type> * Queue<Type>::deQueue() { // remove an item from the front of queue
    /* check whether the queue is normal */
    if(rear == nullptr || front == nullptr) {
        cerr << "the queue is non-existent" << endl;
        return this;
    } else if (isFull()) {
        cout << "the queue is empty" << endl;
        return this;
    }

    /* create a blank node and add it to the rear of queue */
    Node * blankNode = new Node();
    blankNode -> connect(rear);
    rear -> connect_back(blankNode);
    rear = blankNode;

    /* delete the node in the front of queue */
    Node * tmp = front;
    front = front -> getLast() -> resetNext();
    delete tmp;

    items --;

    return this -> layout();
}

template <typename Type>
Queue<Type> * Queue<Type>::clear() { // clear the queue
    items = 0; // simply set the items to zero
    return this;
}



/* Node declaration */

template <typename Type>
class Queue<Type>::Node {

private :
    /* private members */
    static ULL Number; // the number of Nodes
    ULL number; // the number of this Node
    Type data; // the data of this Node
    Node *next; // pointer to the next Node
    Node *last; // pointer to the last Node
    mutable bool ghostNode; // ghost node flag

public :

    /* Construct & Destructor */

    Node(Node *_next = nullptr, Type _data = (Type)0) { // constructor

        cout << "Node constructor" << endl;

        Number ++; // Number self increases when the Node created

        // initialization
        number = 0;
        next = _next;
        data = _data;

        last = nullptr; // the last pointer will be set in the function Anti_Link()

        ghostNode = false; // ghost node flag will be set to true when the Ghost() is called
    }

    ~Node() { // destructor
        Number --;
        if(next != nullptr) {
            delete next;
        }
        cout << "Node destructor" << endl;
    }

    /* Public methods */

    /* the interface of [Number]*/
    /* read only */
    static void showNumber();

    /*the interface of [number & data] */
    /* read only */
    Type show() const; // return the data
    void showAll() const; // show all the data in tht linked list

    /* read and write [number & data] */
    int update_number(int num = -1); // update the number
    Type & getData(); // get the data from the node

    /* the interface of [next pointer] */
    /* read and write */
    bool connect(Node *newNode = nullptr); // connect two nodes by next pointer
    Node * resetNext(); // reset the next pointer
    Node * getNext() const;


    /* the interface of [last pointer] */
    /* read and write */
    bool connect_back(Node *newNode = nullptr); // connect two nodes by last pointer
    Node * resetLast(); // reset the last pointer
    Node * getLast() const;

    /* the interface of [ghostNode] */
    void Ghost() { // set the ghost node flag to true
        ghostNode = true;
    }

};

/* the interface of [Number]*/
template <typename Type>
ULL Queue<Type>::Node::Number = 0;

template <typename Type>
void Queue<Type>::Node::showNumber() {
    cout << "the number of all nodes: " << Number << endl;
}


/*the interface of [number & data] */
template <typename Type>
Type Queue<Type>::Node::show() const{
    cout << "the number of this node is: " << number << endl;
    cout << "the data of this node is: " << data << endl;
    return data;
}

template <typename Type>
void Queue<Type>::Node::showAll() const {
    cout << "show the nodes of linked list from rear to front" << endl;
    this -> show();
    if(this -> next != nullptr) { // use recursive call to traverse the linked list
        this -> next -> showAll();
    }
}

template <typename Type>
int Queue<Type>::Node::update_number(int num) {
    int tmp = number;
    if(num > 0) {
        number = num;
    }
    return tmp;
}

template <typename Type>
Type & Queue<Type>::Node::getData() {
    return data;
}

/* the interface of [next pointer] */
template <typename Type>
bool Queue<Type>::Node::connect(Node *newNode) { // connect two nodes by next pointer
    if(newNode == nullptr) {
        cerr << "nullptr is not allowed" << endl;
        return false;
    }
    next = newNode;
    return true;
}

template <typename Type>
Queue<Type>::Node * Queue<Type>::Node::resetNext() { // reset the next pointer
    next = nullptr;
    return this;
}

template <typename  Type>
Queue<Type>::Node * Queue<Type>::Node::getNext() const {
    return next;
}


/* the interface of [last pointer] */
template <typename Type>
bool Queue<Type>::Node::connect_back(Node *newNode) { // connect two nodes by last pointer
    if(newNode == nullptr) {
        cerr << "nullptr is not allowed" << endl;
        return false;
    }
    last = newNode;
    return true;
}

template <typename Type>
Queue<Type>::Node * Queue<Type>::Node::resetLast() { // reset the last pointer
    last = nullptr;
    return this;
}

template <typename Type>
Queue<Type>::Node * Queue<Type>::Node::getLast() const {
    return last;
}


// template <typename Type>
// void Node<Type>::operator=(Node & node) {
//     data = node.data;
//     next = node.next;
// }





/* String declaration */
/* reference material : "C++ Primer Plus" */

class String {
private :
    /* private members */
    char *str; // a pointer to string
    int len; // the length of string
    static int num_strings; // the number of strings

    static const int CINLIM = 50;

public :
    /* constructor and destructor */
    String(); // default construtor
    String(const char *_str); // constructor
    String(const String &_str); // copy constructor
    ~String(); // destructor

    int length() const { // the interface of len
        return len;
    }

    /* overloaded operator methods */
    String & operator=(const String & _str);
    String & operator=(const char * _str);
    char & operator[](int ord);
    const char & operator[](int i) const;

    /* overloaded operator friends */
    friend bool operator<(const String & str1, const String & str2);
    friend bool operator>(const String & str1, const String & str2);
    friend bool operator==(const String & str1, const String & str2);
    friend ostream & operator<<(ostream & os, const String & _str);
    friend istream & operator>>(istream & is, String & _str);

    /* static function */
    static int HowMany();
};

/* static */

// initialize the static class member
int String::num_strings = 0;

// static methods
int String::HowMany() {
    return num_strings;
}


/* constructor */

String::String() { // default construtor
    len = 0;
    str = new char[1];
    str[0] = '\0'; // default string
    num_strings ++;
}

String::String(const char * _str) { // constructor String from C string
    len = strlen(_str); // set length
    str = new char[len + 1]; // allot storage, here you should plus one cause you have to deposit '\0' at the rear
    strcpy(str, _str); // initialize pointer
    num_strings ++; // update object count
}

String::String(const String & _str) { // copy constructor
    //Note that again the copy function must use deep copy.
    // Otherwise, unpredictable consequences will result.

    // actually, you can also realize this funciton by overloading the '='
    num_strings ++; // update object count
    len = _str.len; // copy the length
    str = new char[len + 1]; // allot space
    strcpy(str, _str.str); // copy string to new location
}

String::~String() { // destructor
    -- num_strings;
    delete [] str;
}


/* overloded operator methods */

String & String::operator=(const String & _str) { // assign a String to String
    if(this == & _str) {
        return *this;
    }
    delete [] str; // delete the old string
    len = _str.len; // copy the length
    str = new char[len + 1]; // allocate new string
    strcpy(str, _str.str); // copy string to new
    return *this;
}

String & String::operator=(const char *_str) { // assign a C to String
    delete [] str;
    len = strlen(_str);
    str = new char[len + 1];
    strcpy(str, _str);
    return *this;
}

/* read-write char access for non-const String */

char & String::operator[](int ord) {
    return str[ord];
}

/* read-only char access for const String */

const char & String::operator[](int ord) const {
    return str[ord];
}


/* overloaded operator friends */

bool operator<(const String & str1, const String & str2) {
    return (strcmp(str1.str, str2.str) < 0);
}

bool operator>(const String & str1, const String & str2) {
    return str2 < str1; // actually you don't need to use strcmp again
}

bool operator==(const String & str1, const String & str2)
{
    return (strcmp(str1.str, str2.str) == 0);
}

ostream & operator<<(ostream & os, const String & _str) {
    os << _str.str;
    return os;
}

istream & operator>>(istream & is, String & _str) {
    char buffer[String::CINLIM];
    is.get(buffer, String::CINLIM);
    if(is) {
        _str = buffer;
    }
    if(is.get() != '\n') {
        cout << "the number of characters entered over limit" << endl;
        cin.ignore(std::numeric_limits<streamsize>::max(), '\n');
    }
    return is;
}




/* Name declaration */

class Name {
private :
    /* private members */
    enum {MAX = 10}; // the maximum length of name
    String name;
    static const char * errMsg; // error message

protected :

    /* protected methods */

    void checkLength(const char * _name) {
        if(strlen(_name) > MAX) {
            throw errMsg;
        }
    }

    void checkLength(const String & _name) {
        if(_name.length() > MAX) {
            throw errMsg;
        }
    }

public :
    /* constructor and destructor */
    Name(const char *_name) {
        checkLength(_name);
        name = _name;
    }

    Name(const String & _name) {
        checkLength(_name);
        name = _name;
    }

    ~Name() {}

    /* the methods use for changing name */
    Name & changeName();
    Name & changeName(const char * newName);
    Name & changeName(const String & newName);
    Name & changeName(const Name & newName);

    bool operator=(const char * newName);
    bool operator=(const String & newName);
    bool operator=(const Name & newName);

    /* overloaded operator friends for comparing */
    friend bool operator==(const Name & name1, const Name & name2);
    friend bool operator>(const Name & name1, const Name & name2);
    friend bool operator<(const Name & name1, const Name & name2);
};

const char * Name::errMsg = "the length of name is over limit";

Name & Name::changeName() {
    cout << "Please input your name" << endl;
    cin >> name;
    checkLength(name);
    return *this;
}

Name & Name::changeName(const char * newName) {
    if(!newName) {
        cerr << "blank name is not allowed" << endl;
        return *this;
    }
    checkLength(newName);
    name = newName;
    return *this;
}

Name & Name::changeName(const String & newName) {
    if(!newName.length()) {
        cerr << "blank name is not allowed" << endl;
        return *this;
    }
    checkLength(newName);
    name = newName;
    return *this;
}

Name & Name::changeName(const Name & newName) {
    this -> name = newName.name;
    return *this;
}

bool Name::operator=(const char * newName) {
    if(newName) {
        changeName(newName);
        return true;
    }
    return false;
}

bool Name::operator=(const String & newName) {
    if(newName.length()) {
        changeName(newName);
        return true;
    }
    return false;
}

bool Name::operator=(const Name & newName) {
    if(newName.name.length()) {
        changeName(newName);
        return true;
    }
    return false;
}

bool operator==(const Name & name1, const Name & name2) {
    return name1.name == name2.name;
}

bool operator>(const Name & name1, const Name & name2) {
    return name1.name > name2.name;
}

bool operator<(const Name & name1, const Name & name2) {
    return name2 > name1;
}




/* Password declaration */

/* account declaration */

/* administrator declaration */

/* user declaration */

/* database declaration */

/* servant declaration*/

// class account {


int main() {
    return 0;
}