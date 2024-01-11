#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int bfs(vector<vector<int>> adj, int s, int e) {
    int n = adj.size();

    vector<bool> visited(n, false);    
    vector<int> dist(n, INT_MAX);

    dist[s] = 0;
    queue<int> q;
    q.push(s);


    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        visited[cur] = true;
        for (auto v : adj[cur]) { 
            if (!visited[v]) {
                dist[v] = dist[cur] + 1;
                q.push(v);
            }
        }
    }

    return dist[e];
}


int main() {

    cout << "Input vertex number, edge number, and edges:" << endl;
    int vertexNum, edgeNum;
    cin >> vertexNum >> edgeNum;
    vector<vector<int>> adjacent( vertexNum );
    for (int i = 0; i < vertexNum; ++i) {
        int from, to;
        cin >> from >> to;
        adjacent[from].push_back( to );
    }

    cout << "Input start and end:" << endl;
    int start, end;
    cin >> start >> end;

    int dist = bfs( adjacent, start, end );

    cout << "The shortest path from " << start << " to " << end << " is " << dist << endl;

    return 0;
}