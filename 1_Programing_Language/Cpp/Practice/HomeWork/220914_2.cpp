#include <iostream>
#include <cstring>

using namespace std;

const int MaxLenOfSamples = 128;

int main() {

    char * hashTable[MaxLenOfSamples*20] = { nullptr };

    int N = 0;
    cin >> N;
    cin.get();

    while (N--) {
        // make a hash table to save the strings
        char * buffer = new char[MaxLenOfSamples]{'\0'};
        cin.getline(buffer, MaxLenOfSamples);
        int ord = strlen(buffer) * 20;
        while (true) {
            if (hashTable[ord] == nullptr) {
                hashTable[ord] = buffer;
                break;
            } else {
                ord += 1;
            }
        }
    }

    for (int i = 0; i < MaxLenOfSamples*20; ++i) {
        if (hashTable[i] != nullptr) {
            cout << hashTable[i] << endl;
            delete hashTable[i];
        }
    }

    return 0;
}