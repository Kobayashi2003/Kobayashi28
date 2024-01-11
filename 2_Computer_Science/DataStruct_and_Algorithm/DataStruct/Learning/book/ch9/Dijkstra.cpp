#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int dijkstra(vector<vector<int>> g, int s, int e) {

    int n = g.size();

    vector<bool> visited(n, false);
    vector<int> dist(n, INT_MAX);
    vector<int> path(n, -1);

    dist[s] = 0;
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    pq.push(make_pair(0, s));

    while (!pq.empty()) {
        int cur = pq.top().second;
        pq.pop();
        visited[cur] = true;

        for (int i = 0; i < n; ++i) {
            if (g[cur][i] != 0 && !visited[i]) {
                if (dist[i] > dist[cur] + g[cur][i]) {
                    dist[i] = dist[cur] + g[cur][i];
                    path[i] = cur;
                    pq.push(make_pair(dist[i], i));
                }
            }
        }
    }

    return dist[e];
}


int main() {

    cout << "Input vertex number, edge number, and edges:" << endl;
    int vertexNum, edgeNum;
    cin >> vertexNum >> edgeNum;
    vector<vector<int>> graph( vertexNum, vector<int>( vertexNum, 0 ) );

    cout << "Input edges:" << endl;
    for (int i = 0; i < edgeNum; ++i) {
        int from, to, weight;
        cin >> from >> to >> weight;
        graph[from][to] = weight;
    }

    cout << "Input start and end:" << endl;
    int start, end;
    cin >> start >> end;

    int dist = dijkstra( graph, start, end );

    cout << "The shortest path from " << start << " to " << end << " is " << dist << endl;

    return 0;
}