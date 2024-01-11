#include <iostream>
#include <vector>
#include <stack>
#include <map>

using namespace std;

template <typename T>
class Graph {

private:

    map<T, vector<T>> adjList;
    map<T, int> inDegree;

public:

    Graph() = default;

    void addEdge(T from, T to);

    void topSort() const;

};

template <typename T>
void Graph<T>::addEdge(T from, T to) {

    adjList[from].push_back(to);
    if (inDegree.find(from) == inDegree.end())
        inDegree[from] = 0;
    inDegree[to]++;

}

template <typename T>
void Graph<T>::topSort() const {

    auto adjList = this->adjList;
    auto inDegree = this->inDegree;

    stack<T> s;
    size_t counter = 0;

    for (auto &item : inDegree)
        if (item.second == 0)
            s.push(item.first);

    while (!s.empty()) {

        counter++;

        T v = s.top();
        s.pop();
        cout << v << " ";

        for (auto &item : adjList[v]) {
            inDegree[item]--;
            if (inDegree[item] == 0)
                s.push(item);
        }

    }

    if (counter != adjList.size())
        cout << "There exists a cycle in the graph" << endl;

}

int main() {

    Graph<char> g;

    g.addEdge('s', 'A');
    g.addEdge('s', 'D');
    g.addEdge('s', 'G');

    g.addEdge('A', 'B');
    g.addEdge('A', 'E');

    g.addEdge('D', 'A');
    g.addEdge('D', 'E');

    g.addEdge('G', 'D');
    g.addEdge('G', 'E');
    g.addEdge('G', 'H');

    g.addEdge('B', 'C');

    g.addEdge('E', 'C');
    g.addEdge('E', 'F');
    g.addEdge('E', 'I');

    g.addEdge('H', 'E');
    g.addEdge('H', 'I');

    g.addEdge('C', 't');

    g.addEdge('F', 't');
    g.addEdge('F', 'C');

    g.addEdge('I', 't');
    g.addEdge('I', 'F');

    g.topSort();

    return 0;
}