// 设计一个算法利用图的遍历方法输出一个无向图G中从顶点Vi到Vj的长度为S的简单路径，设图采用邻接链表作为存储结构。
#include <iostream>
#include <vector>

using namespace std;

struct EdgeNode {
    int adjvex;
    int weight;
    EdgeNode *next;
};

struct VertexNode {
    int vertex;
    EdgeNode *firstedge;
};

class Graph {
private:
    vector<VertexNode> adjList;
    int numVertexes;
    int numEdges;

public:
    Graph(int n, int e) {
        numVertexes = n;
        numEdges = e;
        adjList.resize(n);
        for (int i = 0; i < n; i++) {
            adjList[i].vertex = i;
            adjList[i].firstedge = nullptr;
        }
    }

    void addEdge(int v1, int v2, int w) {
        EdgeNode *e;
        e = new EdgeNode;
        e->adjvex = v2;
        e->weight = w;
        e->next = adjList[v1].firstedge;
        adjList[v1].firstedge = e;

        e = new EdgeNode;
        e->adjvex = v1;
        e->weight = w;
        e->next = adjList[v2].firstedge;
        adjList[v2].firstedge = e;
    }

    void printGraph() {
        EdgeNode *e;
        for (int i = 0; i < numVertexes; i++) {
            cout << adjList[i].vertex << " ";
            e = adjList[i].firstedge;
            while (e != nullptr) {
                cout << e->adjvex << " ";
                e = e->next;
            }
            cout << endl;
        }
    }

    void DFS(int v, int j, int s, vector<int> &path, vector<int> &visited) {
        if (v == j && s == 0) {
            for (int i = 0; i < path.size(); i++) {
                cout << path[i] << " ";
            }
            cout << endl;
            return ;
        }
        visited[v] = 1;
        EdgeNode *e = adjList[v].firstedge;
        while (e != nullptr) {
            if (visited[e->adjvex] == 0) {
                path.push_back(e->adjvex);
                DFS(e->adjvex, j, s - e->weight, path, visited);
                path.pop_back();
            }
            e = e->next;
        }
        visited[v] = 0;
    }

    void findPath(int i, int j, int s) {
        vector<int> path;
        vector<int> visited(numVertexes, 0);
        path.push_back(i);
        DFS(i, j, s, path, visited);
    }
};
        

void test() {
    Graph g(5, 7);
    g.addEdge(0, 1, 1);
    g.addEdge(0, 2, 2);
    g.addEdge(0, 3, 3);
    g.addEdge(1, 2, 4);
    g.addEdge(1, 4, 5);
    g.addEdge(2, 3, 6);
    g.addEdge(3, 4, 7);
    // g.printGraph();
    g.findPath(0, 4, 6);
}

int main() {
    test();
    return 0;
}