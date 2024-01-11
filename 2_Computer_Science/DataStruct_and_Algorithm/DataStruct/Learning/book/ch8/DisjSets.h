#ifndef _DISJSETS_H
#define _DISJSETS_H

#include <vector>

using std::vector;

class DisjSets {
public:
    explicit DisjSets( int numElements );

    int find( int x ) const;
    int find( int x );
    void unionSets( int root1, int root2 );

private:
    vector<int> s;
};

#endif
