#include <iostream>
#include <vector>
#include <unordered_map>
#include <queue>

using namespace std;

// 地图节点的结构体
struct Node {
    int id;                  // 节点标识符
    vector<Node*> neighbors; // 相邻节点
};

// 广度优先搜索函数
bool bfs(Node* start, Node* end, unordered_map<Node*, bool>& visited, unordered_map<Node*, Node*>& parent, unordered_map<Node*, int>& distance) {
    queue<Node*> q;
    q.push(start);
    visited[start] = true;  // 标记起始节点为已访问
    distance[start] = 0;   // 起始节点到自身的距离为0

    while (!q.empty()) {
        Node* curr = q.front();
        q.pop();

        if (curr == end) {
            return true;  // 找到目标节点，搜索结束
        }

        for (Node* neighbor : curr->neighbors) {
            if (!visited[neighbor]) {
                /*============================
                        请在此处完成代码：
                    1. 标记邻居节点为已访问
                    2. 更新邻居节点的父节点
                    3. 更新邻居节点的距离
                    4. 将邻居节点加入队列
                ============================*/
                visited[neighbor] = true;
                parent[neighbor] = curr;
                distance[neighbor] = distance[curr] + 1;
                q.push(neighbor);
            }
        }
    }

    return false;  // 没有找到目标节点
}

// 输出最短路径
void printPath(Node* start, Node* end, unordered_map<Node*, Node*>& parent) {
    vector<int> path;

    Node* curr = end;
    while (curr != start) {
        path.push_back(curr->id);
        curr = parent[curr];
    }

    cout << start->id << " ";
    for (int i = path.size() - 1; i >= 0; --i) {
        cout << path[i] << " ";
    }
    cout << endl;
}

int main() {
    // 构建地图节点
    Node* node1 = new Node{1, {}};
    Node* node2 = new Node{2, {}};
    Node* node3 = new Node{3, {}};
    Node* node4 = new Node{4, {}};
    Node* node5 = new Node{5, {}};
    Node* node6 = new Node{6, {}};
    Node* node7 = new Node{7, {}};
    Node* node8 = new Node{8, {}};
    Node* node9 = new Node{9, {}};

    // 构建节点之间的连接关系
    node1->neighbors = {node2, node3, node4};
    node2->neighbors = {node1, node5};
    node3->neighbors = {node1, node4, node6};
    node4->neighbors = {node1, node3, node7, node9};
    node5->neighbors = {node2, node8};
    node6->neighbors = {node3, node9};
    node7->neighbors = {node4};
    node8->neighbors = {node5};
    node9->neighbors = {node4, node6};

    // 起始节点和目标节点
    int startId, endId;
    cin >> startId >> endId;

    Node* start = nullptr;
    Node* end = nullptr;

    // 查找起始和目标节点
    for (Node* node : {node1, node2, node3, node4, node5, node6, node7, node8, node9}) {
        if (node->id == startId)
            start = node;
        if (node->id == endId)
            end = node;
    }

    if (start == nullptr || end == nullptr) {
        cout << "输入的起始或结束节点标识符无效！" << endl;
        return 0;
    }

    unordered_map<Node*, bool> visited;
    unordered_map<Node*, Node*> parent;
    unordered_map<Node*, int> distance;

    // 进行广度优先搜索
    if (bfs(start, end, visited, parent, distance)) {
        // 输出最短路径
        printPath(start, end, parent);
    } else {
        cout << "No path found!" << endl;
    }

    // 释放内存
    delete node1;
    delete node2;
    delete node3;
    delete node4;
    delete node5;
    delete node6;
    delete node7;
    delete node8;
    delete node9;

    return 0;
}
