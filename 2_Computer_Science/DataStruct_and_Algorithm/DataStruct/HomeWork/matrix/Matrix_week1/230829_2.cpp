#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {

    string str; getline(cin, str);
    vector<string> words = {""};

    for (auto ch : str) 
        if (ch == ' ')
            words.push_back("");
        else
            words[words.size()-1] += ch;
        
    for (auto word : words) {
        for (int i = word.size()-1; i >= 0; --i)
            cout << word[i];
        cout << " ";
    }

    return 0;
}