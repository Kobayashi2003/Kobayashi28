#ifndef _DISJSETS_H
#define _DISJSETS_H

#include <vector>

using std::vector;


template <typename Object>
class DisjSets {

public:

    explicit DisjSets( vector<Object> & v ) : s( v.size(), -1 ), v( v ) { }

    int findAncestor( int x ) {
        if ( s[x] < 0 )
            return x;
        else 
            return findAncestor( s[x] );
    }

    bool isSameSet( int x, int y ) {
        return findAncestor( x ) == findAncestor( y );
    }

    void unionSets( int x, int y ) {
        int root1 = findAncestor( x );
        int root2 = findAncestor( y );

        if ( root1 == root2 )
            return ;

        s[root2] = root1;
    }

private:

    vector<int> s;
    vector<Object> v;

};


#endif