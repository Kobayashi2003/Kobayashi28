#include <iostream>
#include <string>
using namespace std;

class Word_list
{
private:
    string *_word_list; //存放拆分出来的单词的数组，允许重复
    int _N; //“_word_list”的长度，也即可以容纳的单词个数——注意是“最大”容量
public:
    Word_list(int N); //要求“_word_list”的所有元素初始化为空字符串，即""
    ~Word_list();
    void extract_words(string senetance); //将输入的字符串“sentence”拆分成一个个单词并按照先后顺序存入“_word_list”
    string get_words(int index); //获取“_word_list”中的第“index”个单词
    int get_N();                 //获取“_word_list”的单词容量
};

//你的代码会从这里插入

Word_list::Word_list(int N) : _N(N) {
    _word_list = new string[_N];
    for (int i = 0; i < _N; i++) {
        _word_list[i] = "";
    }
}

Word_list::~Word_list() {
    delete [] _word_list;
}

void Word_list::extract_words(string sentence) {
    int index = 0;
    for (int i = 0; i < (int)sentence.length(); ++i) {
        if (sentence[i] == ' ') {
            index++;
        } else if(sentence[i] == ',' || sentence[i] == '.' ||
                  sentence[i] == '!' || sentence[i] == '?') {
            continue;
        } else {
            _word_list[index] += sentence[i];
        }
    }
}

string Word_list::get_words(int index) {
    return _word_list[index];
}

int Word_list::get_N() {
    return _N;
}

int main()
{
    int N;
    cin >> N; //输入的“N”必定比“sentence”的单词个数大
    string sentence;
    getline(cin, sentence); //清空缓存区用
    getline(cin, sentence);
    Word_list a(N);
    a.extract_words(sentence);
    //打印拆分后的单词
    for (int i = 0; i < a.get_N(); i++)
    {
        if (a.get_words(i) != "")
            cout << a.get_words(i) << endl;
        else
            break; //如果当前位置为空字符串，则后面位置均为空字符串，没有单词信息，无需打印
    }
    return 0;
}