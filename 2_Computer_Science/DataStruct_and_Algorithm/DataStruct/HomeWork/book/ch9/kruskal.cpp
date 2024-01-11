#include <iostream> 

#include <vector>
#include <queue>
#include "DisjSets.h"

using namespace std;

struct Edge {

    int u, v, w;

    Edge(int _u, int _v, int _w) : u(_u), v(_v), w(_w) { }

    bool operator > (const Edge& rhs) const {
        return w > rhs.w;
    }
};


vector<Edge> kruskal( vector<Edge> edges, size_t numVectices ) {

    vector<Edge> mst;
    DisjSets<Edge> ds{ edges };
    priority_queue<Edge, vector<Edge>, greater<Edge>> pq;

    for ( auto & e : edges )
        pq.push( e );

    while ( mst.size() != numVectices - 1 ) {
        Edge e = pq.top();
        pq.pop();

        if ( !ds.isSameSet( e.u, e.v ) ) {
            // recieve the edge
            mst.push_back( e );
            ds.unionSets( e.u, e.v );
        }
    }

    return mst;    
}

int main() {

    vector<Edge> edges;
    
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

    edges.push_back( Edge( 5, 1, 4 ) );
    edges.push_back( Edge( 5, 2, 2 ) );
    edges.push_back( Edge( 5, 4, 5 ) );
    edges.push_back( Edge( 5, 8, 2 ) );
    edges.push_back( Edge( 5, 9, 1 ) );

    edges.push_back( Edge( 5, 6, 11 ) );

    edges.push_back( Edge( 6, 2, 3 ) );
    edges.push_back( Edge( 6, 3, 6 ) );
    edges.push_back( Edge( 6, 7, 2 ) );
    edges.push_back( Edge( 6, 9, 3 ) );
    edges.push_back( Edge( 6, 10, 11 ) );

    edges.push_back( Edge( 1, 2, 3 ) );
    edges.push_back( Edge( 2, 3, 10 ) );
    edges.push_back( Edge( 3, 7, 1 ) );
    edges.push_back( Edge( 7, 10, 8 ) );
    edges.push_back( Edge( 10, 9, 7 ) );
    edges.push_back( Edge( 9, 8, 4 ) );
    edges.push_back( Edge( 8, 4, 6 ) );
    edges.push_back( Edge( 4, 1, 4 ) );

    auto mst = kruskal( edges, 10 );

    for ( auto & e : mst )
        cout << e.u << " " << e.v << " " << e.w << endl;

    return 0;
}