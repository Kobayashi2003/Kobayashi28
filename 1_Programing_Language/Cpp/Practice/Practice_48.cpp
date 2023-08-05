#include<iostream>
#include<string>

using namespace std;

int errNum = 0;
const char * errStr = "Wrong";
string errObj = "Erro";;

int main() {
    int state;
    while (cin >> state) {
        try {
            switch(state) {
                case 0 :
                    throw errNum;
                    break;
                case 1 :
                    throw errStr;
                    break;
                case 2 :
                    throw errObj;
                    break;
                default :
                    cout << "normal" << endl;
            }
        } catch (int errMsg) {
            cout << errMsg << endl;
        } catch (const char * errMsg) {
            cout << errMsg << endl;
        } catch (string errMsg) {
            cout << errMsg << endl;
        }
    }
    return 0;
}