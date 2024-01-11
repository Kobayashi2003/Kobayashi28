#include <iostream>
#include <string>
#include <cstring>
using namespace std;

struct HFMNode {
    int w;
    char ch;
    string code;
    int lchild, rchild, parent;
};

class HFMCode {
public:
    HFMCode(string str, int n) {
        //构造哈夫曼树
        leafSize = n;
        HFMTree = new HFMNode[2 * leafSize - 1];
        for (int i = 0; i < 2 * leafSize - 1; i++) {
            HFMTree[i].w = 0;
            HFMTree[i].ch = '\0';
            HFMTree[i].code = "";
            HFMTree[i].lchild = -1;
            HFMTree[i].rchild = -1;
            HFMTree[i].parent = -1;
        }
        for (auto ch : str) {
            for (int i = 0; i < leafSize; ++i) {
                if (HFMTree[i].ch == ch) {
                    HFMTree[i].w++;
                    break;
                }
                if (HFMTree[i].ch == '\0') {
                    HFMTree[i].ch = ch;
                    HFMTree[i].w++;
                    break;
                }
            }
        }
        for (int i = leafSize; i < 2*leafSize-1; ++i) {
            int min1, min2;
            select(min1, min2, i);
            HFMTree[min1].parent = HFMTree[min2].parent = i;
            HFMTree[i].lchild = min1;
            HFMTree[i].rchild = min2;

            HFMTree[i].w = HFMTree[min1].w + HFMTree[min2].w;
            HFMTree[min1].w = HFMTree[min2].w =  0x7fffffff;
        }
    }

    void select(int &min1, int &min2, int parent) {
        //构造哈夫曼树时每次从权值序列选取（从左到右选取）两个最小的权值，详见题目说明
        int min = 0x7fffffff;
        for (int i = 0; i < parent; i++) {
            if (HFMTree[i].parent == -1 && HFMTree[i].w < min) {
                min = HFMTree[i].w;
                min1 = i;
            }
        }
        min = 0x7fffffff;
        for (int i = 0; i < parent; i++) {
            if (HFMTree[i].parent == -1 && HFMTree[i].w < min && i != min1) {
                min = HFMTree[i].w;
                min2 = i;
            }
        }
    }

    void getcode(string str) {
        //根据哈夫曼树求出每个字符的哈夫曼编码
        for (int i = 0; i < leafSize; ++i) {
            int parent = i;
            while (HFMTree[parent].parent != -1) {
                if (HFMTree[HFMTree[parent].parent].lchild == parent) {
                    HFMTree[i].code = "0" + HFMTree[i].code;
                } else {
                    HFMTree[i].code = "1" + HFMTree[i].code;
                }
                parent = HFMTree[parent].parent;
            }
        }

        for (auto ch : str)
            for (int i = 0; i < leafSize; ++i)
                if (HFMTree[i].ch == ch)
                    cout << HFMTree[i].code;
        cout << endl;
    }

private:
    HFMNode *HFMTree;
    int leafSize;
};

int main() {
    int N;
    cin >> N;
    string str;
    cin >> str;
    HFMCode hfmtree(str, N);
    hfmtree.getcode(str);
    return 0;
}
