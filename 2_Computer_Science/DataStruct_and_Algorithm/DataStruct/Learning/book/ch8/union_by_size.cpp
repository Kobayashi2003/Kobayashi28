#include "DisjSets.h"

/*
    * Construct the disjoint sets object.
    * for simplicity, we assume root1 and root2 are distinct
    * and represent set names.
    * root1 is the root of set 1.
    * root2 is the root of set 2.
*/
void DisjSets::unionSets( int root1, int root2 ) { // union by size
    if (s[root2] < s[root1]) {
        s[root1] += s[root2];
        s[root2] = root1;
    } else {
        s[root2] += s[root1];
        s[root1] = root2;
    }
}

/*
    * Perfrom a find with path compression.
    * Error checks omitted again for simplicity.
    * Return the set containing x.
*/
int DisjSets::find( int x ) {
    if ( s[x] < 0 )
        return x;
    else
        return s[x] = find( s[x] );
}