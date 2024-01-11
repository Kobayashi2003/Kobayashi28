#ifndef DISJ_SETS_H
#define DISJ_SETS_H

#include <vector>

using namespace std;

class DisjSets {
private:
    vector<int> s; 

public:
    explicit DisjSets( int numElements ) : s( numElements, -1 ) { }

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

        // you can make the first set the root of the second set
        // or the second set the root of the first set
        // just depends on your preference
        s[root2] = root1;
    }


    void unionSets_by_height( int x, int y ) {
        int root1 = findAncestor( x );
        int root2 = findAncestor( y );

        if ( root1 == root2 )
            return ;

        if ( s[root2] < s[root1] ) {
            s[root1] = root2;
        } else {
            if ( s[root1] == s[root2] )
                --s[root1];
            s[root2] = root1;
        }

    }


    void unionSets_by_size( int x, int y ) {
        int root1 = findAncestor( x );
        int root2 = findAncestor( y );

        if ( root1 == root2 )
            return ;

        if ( s[root2] < s[root1] ) {
            s[root2] += s[root1];
            s[root1] = root2;
        } else {
            s[root1] += s[root2];
            s[root2] = root1;
        }
    }


    typedef vector<int>::iterator iterator;
    typedef vector<int>::const_iterator const_iterator;

    iterator begin() { return s.begin(); }
    const_iterator begin() const { return s.begin(); }
    iterator end() { return s.end(); }
    const_iterator end() const { return s.end(); }
};

#endif