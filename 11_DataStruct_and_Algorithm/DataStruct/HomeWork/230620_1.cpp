#include<iostream>
#define MAX_W 10000
using namespace std;

int dijkstra(int N, int M, int E[][3], int v1, int v2) {
	// N：顶点数 M：边数 E：顶点和距离 v1 v2：顶点，编号从1开始

	int* S = new int[N];	  // 已经找到了最短路径的顶点的集合
	int* dist = new int[N];   // v1到每个顶点的最短距离

	for (int i = 0; i < N; i++) {
		S[i] = 0;
		dist[i] = MAX_W;
	}
	// S[v1 - 1] = 1;
    S[v1 - 1] = 0;
	dist[v1 - 1] = 0;

	/*
		请完成dijkstra算法代码
	*/

    while ( true ) {
        int min = MAX_W;
        int min_index = -1;
        for (int i = 0; i < N; ++i) {
            if (S[i] == 0 && dist[i] < min) {
                min = dist[i];
                min_index = i;
            }
        }

        if (min_index == -1) {
            break;
        }

        S[min_index] = 1;

        for (int i = 0; i < M; ++i) {
            if (E[i][0] == min_index + 1) { // adjacent vertex
                int adj = E[i][1] - 1;
                if (S[adj] == 0 && dist[adj] > dist[min_index] + E[i][2]) {
                    dist[adj] = dist[min_index] + E[i][2];
                }
            }
        }

    }

	int result = dist[v2 - 1] == MAX_W ? -1 : dist[v2 - 1];

	delete []S;
	delete []dist;
	return result;
}
int main() {
	int N, M, v1, v2;
	cin >> N >> M >> v1 >> v2;
	int(*E)[3] = new int[M][3];    // E[i][0]：顶点a， E[i][1]：顶点b， E[i][2]：a到b的距离
	for (int i = 0; i < M; i++)
		cin >> E[i][0] >> E[i][1] >> E[i][2];

	cout << dijkstra(N, M, E, v1, v2);

	delete []E;
	return 0;
}