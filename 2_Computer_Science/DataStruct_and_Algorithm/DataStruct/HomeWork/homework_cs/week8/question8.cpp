#include <iostream>
#include <vector>

using namespace std;

const int INF = 1000000;

/*
0 & 5 & 3 & . & . & . \\
. & 0 & . & . & 9 & 4 \\
. & . & 0 & 2 & 5 & . \\
. & . & . & 0 & 4 & . \\
6 & . & . & . & 0 & . \\
. & . & . & . & 3 & 0 \\
*/

int graph[6][6] = {
    {0, 5, 3, INF, INF, INF},
    {INF, 0, INF, INF, 9, 4},
    {INF, INF, 0, 2, 5, INF},
    {INF, INF, INF, 0, 4, INF},
    {6, INF, INF, INF, 0, INF},
    {INF, INF, INF, INF, 3, 0}};


void floyd(int graph[][6], int n) {
    int dist[n][n];

    // init
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; j++)
            dist[i][j] = graph[i][j];
    
    // floyd
    for (int k = 0; k < n; ++k) {
        // choose k as the intermediate point
        for (int i = 0; i < n; ++i) {
            // choose i as the start point
            for (int j = 0; j < n; ++j) {
                // choose j as the end point
                if (dist[i][k] + dist[k][j] < dist[i][j])
                    dist[i][j] = dist[i][k] + dist[k][j]; 
            }
        }
    }

    // print
    for (int i = 0; i < n; ++i) {
        cout << "From " << char(i + 'A') << " to: " << endl;
        for (int j = 0; j < n; ++j) {
            cout << "    " << char(j + 'A') << ": " << dist[i][j] << endl;
        }
    }
}

int main() {
    floyd(graph, 6);
    return 0;
}