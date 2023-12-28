#include <iostream>
#include <vector>

using namespace std;
    
const int N = 9;

class Solution {
public:
    bool graph[N][N];
    vector<vector<int>> results;

    Solution() {
        for (int i = 0; i < N; ++i) 
            for (int j = 0; j < N; ++j) 
                graph[i][j] = false;

        for (int i = 0; i < N; ++i) 
            visited.push_back(false);
    }

private:

    vector<int> indegree;
    vector<bool> visited;
    vector<int> path;

    void count_indegree(vector<int> & indegree) {
        for (int i = 0; i < N; ++i) 
        {
            int cnt_indegree = 0;
            for (int j = 0; j < N; ++j) 
            {
                if (graph[j][i]) 
                {
                    cnt_indegree++;
                }
            }
            indegree.push_back(cnt_indegree);
        }
    }

    void top_sort() {

        if (path.size() == N) 
        {
            results.push_back(path);
            return ;
        }

        for (int i = 0; i < N; ++i) 
        {
            if (indegree[i] == 0 && !visited[i]) 
            {
                // chose i
                path.push_back(i);
                visited[i] = true;
                for (int j = 0; j < N; ++j) 
                {
                    if (graph[i][j]) 
                        indegree[j] -= 1;
                }

                top_sort();

                // unchose i
                for (int j = 0; j < N; ++j) 
                {
                    if (graph[i][j])
                        indegree[j] += 1;
                }
                visited[i] = false;
                path.pop_back();
            }
        }
    }

public:

    void find_all_top_sort() {
        count_indegree(indegree);
        top_sort();
    }

};


int main() {

    Solution s;

    s.graph[0][1] = true;
    s.graph[1][3] = true;
    s.graph[2][4] = true;
    s.graph[3][2] = true;
    s.graph[3][6] = true;
    s.graph[5][4] = true;
    s.graph[6][5] = true;
    s.graph[7][5] = true;
    s.graph[8][7] = true;
    s.graph[8][6] = true;

    s.find_all_top_sort();

    for (int i = 0; i < s.results.size(); ++i) {
        for (int j = 0; j < s.results[i].size(); ++j) {
            cout << s.results[i][j]+1 << " ";
        }
        cout << endl;
    }

    return 0;
}