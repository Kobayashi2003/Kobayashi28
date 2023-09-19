struct Node{
    Node* next;
    int value;
    Node(int val):value(val),next(nullptr){}
};

Node* ReverseMergeList(Node* List1, Node* List2) {
    Node* head = new Node(0);
    Node *p1 = List1, *p2 = List2;
    while (p1 != nullptr && p2 != nullptr) {
        Node *newNode = nullptr;
        if (p1->value < p2->value) {
            newNode = new Node(p1->value);
            p1 = p1->next; 
        } else {
            newNode = new Node(p2->value);
            p2 = p2->next;
        }
        newNode->next = head->next;
        head->next = newNode;
    }
    Node *restList = p1 == nullptr ? p2 : p1;
    while (restList != nullptr) {
        Node *newNode = new Node(restList->value);
        newNode->next = head->next;
        head->next = newNode;
        restList = restList->next;
    }
    Node *tmp = head;
    head = head->next;
    delete tmp;
    return head;
}