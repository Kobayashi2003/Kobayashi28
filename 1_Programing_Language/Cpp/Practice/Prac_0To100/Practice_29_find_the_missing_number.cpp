#include<iostream>
#include<vector>

using namespace std;

void findMissingNumber(vector <int> &numbers) {
    // for(int i = 0; (unsigned int)i < numbers.size(); ++i) {
    //     if(i != numbers[i]) {
    //         cout << "the missing number is: " << i << endl;
    //         return;
    //     }
    // }

    int x = 0;
    for(int i = 0; (unsigned int)i <= numbers.size(); ++i) {
        x ^= i;
        x = ((unsigned int)i < numbers.size() ? x ^ numbers[i] : x);
    }
    cout << "the missing number is: " << x << endl;
}

int main() {
    int n;
    cout << "Please enter the number of numbers: " ;
    cin >> n;

    vector <int> numbers(n);
    // cout << "Pleaase enter the numbers:" << endl;
    // for(int i = 0; i < n; i++) {
    //     cin >> numbers[i];
    // }

    int missNum;
    cout << "Please design the number you want to hide: ";
    cin >> missNum;
    for(int i = 0, j = 0; i < n; i++) {
        if(j == missNum) {
            j ++;
        }
        numbers[i] = j++;
    }

    findMissingNumber(numbers);

    return 0;
}