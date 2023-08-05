#include<iostream>
#include<string>
using namespace std;

class Pair {
private:
	string _word;        //单词
	int    _freq;        //出现次数
public:
	Pair();
	~Pair();
	int    get_freq();
	string get_word();
	void   set_freq(int freq);
	void   set_word(string word);
};

class Word_freq_profile {//单词统计概览列表
private:
	int   _N;        //“_list”的长度，也即单词“最大”容量
	Pair* _list;     //存放单词和频次信息的数组
public:
	Word_freq_profile(int N);
	Word_freq_profile(const Word_freq_profile& src);//复制拷贝函数
	~Word_freq_profile();
	Pair get_Pair(int index) const;          //获取_list的第index位
	int get_N() const;
	void add(string src);  //如果src已经在列表里出现，那么相应的位置频率自增1，如果不在列表里，在列表的末尾增加单词，频率设1
	                       //注意：列表的末尾指的是第一个没有单词信息的位置！！！而不是_list[_N-1]
	void show();
};

class Word_list {
private:
	string* _word_list;
	int     _N;
public:
	Word_list(int N);
	~Word_list();
	void extract_words(string senetance); //拆分句子得到所有单词并存入_word_list
	string get_words(int index);          //获取_word_list的第index位
	int get_N();
	Word_freq_profile get_freq_profile();  //对拆分出来的所有单词进行统计
};

//你的代码从这里插入

/* Pair function */
Pair::Pair() = default;

Pair::~Pair() = default;

int Pair::get_freq() { return _freq; }

string Pair::get_word() { return _word; }

void Pair::set_freq(int freq) { _freq = freq; }

void Pair::set_word(string word) { _word = word; }
/* Pair function end */


/* Word_freq_profile function */
Word_freq_profile::Word_freq_profile(int N) : _N(N) { _list = new Pair[N]; }

Word_freq_profile::Word_freq_profile(const Word_freq_profile& src) {
    _N = src._N;
    _list = new Pair[_N];
    for (int i = 0; i < _N; i++) {
        _list[i] = src._list[i];
    }
}

Word_freq_profile::~Word_freq_profile() { delete[] _list; }

Pair Word_freq_profile::get_Pair(int index) const { return _list[index]; }

int Word_freq_profile::get_N() const { return _N; }

void Word_freq_profile::add(string src) {
    int i = 0;
    for (i = 0; i < _N && _list[i].get_word() != ""; i++) {
        if (_list[i].get_word() == src) {
            _list[i].set_freq(_list[i].get_freq() + 1);
            return;
        }
    }
    _list[i].set_word(src);
    _list[i].set_freq(1);
}

void Word_freq_profile::show() {
    // sort by word
    for (int i = 0; i < _N - 1; i++) {
        for (int j = i + 1; j < _N && _list[j].get_word() != ""; j++) {
            if (_list[i].get_word() > _list[j].get_word()) {
                Pair temp = _list[i];
                _list[i] = _list[j];
                _list[j] = temp;
            }
        }
    }
    for (int i = 0; i < _N && _list[i].get_word() != ""; i++) {
        cout << _list[i].get_word() << " " << _list[i].get_freq() << endl;
    }
}
/* Word_list function end */


/* Word_list function*/
Word_list::Word_list(int N) : _N(N) {
    _word_list = new string[_N];
    for (int i = 0; i < _N; i++) {
        _word_list[i] = "";
    }
}

Word_list::~Word_list() { delete [] _word_list; }

void Word_list::extract_words(string sentence) {
    // change the sentence to lower cases
    for (int i = 0; i < (int)sentence.length(); i++) {
        if (sentence[i] >= 'A' && sentence[i] <= 'Z') {
            sentence[i] += 32;
        }
    }

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

string Word_list::get_words(int index) { return _word_list[index]; }

int Word_list::get_N() { return _N; }

Word_freq_profile Word_list::get_freq_profile() {
    Word_freq_profile profile(_N);
    for (int i = 0; i < _N; i++) {
        profile.add(_word_list[i]);
    }
    return profile;
}
/* Word_list function end*/

int main() {
	int N;
	cin >> N;
	string sentence;
	getline(cin, sentence);//清空缓存区用
	getline(cin, sentence);
	Word_list a(N);
	a.extract_words(sentence);
	Word_freq_profile b = a.get_freq_profile();
	b.show();
	return 0;
}