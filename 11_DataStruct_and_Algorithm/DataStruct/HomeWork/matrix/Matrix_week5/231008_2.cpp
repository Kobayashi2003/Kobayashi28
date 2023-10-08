#include <string>
#include <stack>

using namespace std;

bool isValid(string s);

bool isValid(string str) {

    stack <char> brackets;

    for (char c : str) {
        if (c == '(' || c == '[' || c == '{') {
            brackets.push(c); continue;
        }
        if (brackets.empty() || abs(c-brackets.top()) > 2) return false;
        brackets.pop();
    }   

    return brackets.empty();
}
