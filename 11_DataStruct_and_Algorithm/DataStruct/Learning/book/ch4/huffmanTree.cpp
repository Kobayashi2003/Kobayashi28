#include <iostream>
#include <string>
#include <map>

using namespace std;

class huffmanTree {

private:
    struct huffmanNode {
        int weight;
        char ch;
        string code;
        int lchild, rchild, parent;
    };

    map<char, int> weightMap;
    huffmanNode * HFMTree;
    int leafSize;

    void makeWeightMap(const string & str) {
        for (auto ch : str) {
            if (weightMap.find(ch) == weightMap.end()) {
                weightMap[ch] = 1;
            } else {
                weightMap[ch]++;
            }
        }
    }

    void select2min(int &min1, int &min2, int i) {
        int min = 0x7fffffff;
        for (int j = 0; j < i; ++j) {
            if (HFMTree[j].weight < min && HFMTree[j].parent == -1) {
                min = HFMTree[j].weight;
                min1 = j;
            }
        }
        min = 0x7fffffff;
        for (int j = 0; j < i; ++j) {
            if (HFMTree[j].weight < min && HFMTree[j].parent == -1 && j != min1) {
                min = HFMTree[j].weight;
                min2 = j;
            }
        }
    }

    void makeHuffmanCode(const string & str) {
        for (int i = leafSize; i < 2 * leafSize - 1; ++i) {
            int min1, min2;
            select2min(min1, min2, i);
            HFMTree[min1].parent = HFMTree[min2].parent = i;
            HFMTree[i].lchild = min1;
            HFMTree[i].rchild = min2;
            HFMTree[i].weight = HFMTree[min1].weight + HFMTree[min2].weight;
            HFMTree[min1].weight = HFMTree[min2].weight = 0x7fffffff;
        }

        for (int i = 0; i < leafSize; ++i) {
            int cur = i;
            int parent = HFMTree[cur].parent;
            while (parent != -1) {
                if (HFMTree[parent].lchild == cur) {
                    HFMTree[i].code = "0" + HFMTree[i].code;
                } else {
                    HFMTree[i].code = "1" + HFMTree[i].code;
                }
                cur = parent;
                parent = HFMTree[cur].parent;
            }
            codeMap[HFMTree[i].ch] = HFMTree[i].code;
        }
    }

public:
    huffmanTree(const string & str) {
        makeWeightMap(str);
        leafSize = weightMap.size();
        HFMTree = new huffmanNode[2 * leafSize - 1];
        for (int i = 0; i < 2 * leafSize - 1; ++i) {
            HFMTree[i].weight = 0;
            HFMTree[i].ch = '\0';
            HFMTree[i].code = "";
            HFMTree[i].lchild = -1;
            HFMTree[i].rchild = -1;
            HFMTree[i].parent = -1;
        }
        for (int i = 0; i < leafSize; ++i) {
            HFMTree[i].ch = weightMap.begin()->first;
            HFMTree[i].weight = weightMap.begin()->second;
            weightMap.erase(weightMap.begin());
        }   
        makeHuffmanCode(str);
        for (auto it = codeMap.begin(); it != codeMap.end(); ++it) {
            cout << it->first << " " << it->second << endl;
        }
        for (auto ch : str) {
            huffmanCode += codeMap[ch];
        }
    }

public:
    string huffmanCode;
    map<char, string> codeMap;
};

int main() {

    string str = "this is an example for huffman tree";
    huffmanTree hfmTree(str);
    cout << hfmTree.huffmanCode << endl;

    return 0;
}