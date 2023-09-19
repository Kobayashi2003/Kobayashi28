struct Node{
	Node* prior;
    Node* next;
    int data;
    int freq;
    Node(int val, int fre):data(val),freq(fre),prior(nullptr),next(nullptr){}
};


Node* Locate(Node* head, int x);

Node* Locate(Node* head, int x) {
    if (head == nullptr) 
        return nullptr;

    Node* cur = head;

    while (cur != nullptr) {
        if (cur->data == x) {
            cur->freq++;
            break;
        }
        cur = cur->next;
    }

    while (cur != nullptr && cur->prior != nullptr) {
        if (cur->freq > cur->prior->freq) {
            int tmp = cur->freq;
            cur->freq = cur->prior->freq;
            cur->prior->freq = tmp;
            tmp = cur->data;
            cur->data = cur->prior->data;
            cur->prior->data = tmp;
        }
        cur = cur->prior;
    }

    return head;
}