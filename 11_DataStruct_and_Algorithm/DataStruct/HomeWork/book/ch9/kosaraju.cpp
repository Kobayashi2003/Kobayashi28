#include <iostream>
#include <vector>
#include <stack>

using namespace std;

class Graph {

public:

    Graph( size_t numVertices )
        : adjList( numVertices ), indgree( numVertices ) { }

    void addEdge( int u, int v ) {
        adjList[u].push_back( v );
        ++indgree[v];
    }

    void dfs1( stack<int> & s, vector<bool> & visited, int v ) {
        visited[v] = true;
        
        for ( size_t i = 0; i < adjList[v].size(); ++i ) {
            int next = adjList[v][i];
            if ( !visited[next] )
                dfs1( s, visited, next );
        }

        s.push( v );
    }

    void dfs2( vector<int> & path, vector<bool> & visited, int v ) {
        visited[v] = true;

        path.push_back( v );

        for ( size_t i = 0; i < adjList[v].size(); ++i ) {
            int next = adjList[v][i];
            if ( !visited[next] )
                dfs2( path, visited, next );
        }
    }

    void reverseAdjList() {
        vector< vector<int> > newAdjList( adjList.size() );
        vector<int> newIndgree( adjList.size() );

        for ( size_t i = 0; i < adjList.size(); ++i ) {
            for ( size_t j = 0; j < adjList[i].size(); ++j ) {
                int v = adjList[i][j];
                newAdjList[v].push_back( i );
                ++newIndgree[i];
            }
        }

        adjList = newAdjList;
        indgree = newIndgree;
    }

    vector<vector<int>> kosaraju() {
        vector<vector<int>> result;

        stack<int> order;
        vector<bool> visited( adjList.size(), false );

        for ( size_t i = 0; i < adjList.size(); ++i ) {
            if ( !indgree[i] ) {
                dfs1( order, visited, i );
                break;
            }
        }

        visited.assign( adjList.size(), false );
        reverseAdjList();

        while ( !order.empty() ) {
            int v = order.top();
            order.pop();

            if ( !visited[v] ) {
                vector<int> path;
                dfs2( path, visited, v );
                result.push_back( path );
            }
        }

        return result;
    }

private:

    vector< vector<int> > adjList;
    vector<int> indgree;

};


int main() {

    /*
        * A-G 0-6
        * A->B
        * A->C
        * B->C
        * B->E
        * B->G
        * C->D
        * C->E
        * E->F
        * E->D
        * D->F
        * D->A
        * G->E
    */

    Graph g( 7 );
    g.addEdge( 0, 1 );
    g.addEdge( 0, 2 );
    g.addEdge( 1, 2 );  
    g.addEdge( 1, 4 );
    g.addEdge( 1, 6 );
    g.addEdge( 2, 3 );
    g.addEdge( 2, 4 );
    g.addEdge( 4, 5 );
    g.addEdge( 4, 3 );
    g.addEdge( 3, 5 );
    g.addEdge( 3, 0 );
    g.addEdge( 6, 4 );

    g.reverseAdjList();
    vector<vector<int>> result = g.kosaraju();

    for ( size_t i = 0; i < result.size(); ++i ) {
        cout << "Strong component " << i+1 << ": ";
        for ( size_t j = 0; j < result[i].size(); ++j )
            cout << char(result[i][j] + 'A') << " ";
        cout << endl;
    }

    return 0;
}