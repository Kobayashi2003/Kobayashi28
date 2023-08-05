#include <iostream>

#include <vector>
#include <queue>


using namespace std;

class Graph {

public:

    explicit Graph( size_t numVertices )
        : adjList( numVertices ), weight( numVertices ) { }

    void addEdge( int u, int v, int w ) {
        adjList[u].push_back( v );
        adjList[v].push_back( u );

        weight[u].push_back( w );
        weight[v].push_back( w );
    }

    void prim( int start ) {
        
        vector<bool> visited( adjList.size(), false );
        priority_queue< pair<int, int>, vector< pair<int, int> >, greater< pair<int, int> > > pq;

        // pair<weight, vertex>
        pq.push( make_pair( 0, start ) );

        while ( !pq.empty() ) {
            pair<int, int> p = pq.top();
            pq.pop();

            if ( visited[p.second] )
                continue;

            visited[p.second] = true;

            cout << p.second << " ";

            for ( size_t i = 0; i < adjList[p.second].size(); ++i ) {
                int v = adjList[p.second][i];
                int w = weight[p.second][i];

                if ( !visited[v] )
                    pq.push( make_pair( w, v ) );
            }
        }
    }    

private:

    vector< vector<int> > adjList;
    vector< vector<int> > weight;

};



int main() {

    Graph g( 11 );
    /*
        A-J 1-10

        E-A 4
        E-B 2
        E-D 5
        E-H 2
        E-I 1

        E-F 11

        F-B 3
        F-C 6
        F-G 2
        F-I 3
        F-J 11
        
        A-B 3
        B-C 10
        C-G 1
        G-J 8
        J-I 7
        I-H 4
        H-D 6
        D-A 4

    */

    g.addEdge( 5, 1, 4 );
    g.addEdge( 5, 2, 2 );
    g.addEdge( 5, 4, 5 );
    g.addEdge( 5, 8, 2 );
    g.addEdge( 5, 9, 1 );

    g.addEdge( 5, 6, 11 );

    g.addEdge( 6, 2, 3 );
    g.addEdge( 6, 3, 6 );
    g.addEdge( 6, 7, 2 );
    g.addEdge( 6, 9, 3 );
    g.addEdge( 6, 10, 11 );

    g.addEdge( 1, 2, 3 );
    g.addEdge( 2, 3, 10 );
    g.addEdge( 3, 7, 1 );
    g.addEdge( 7, 10, 8 );
    g.addEdge( 10, 9, 7 );
    g.addEdge( 9, 8, 4 );
    g.addEdge( 8, 4, 6 );
    g.addEdge( 4, 1, 4 );

    g.prim( 1 );

    return 0;
}